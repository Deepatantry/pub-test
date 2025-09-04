from typing import List, Dict, Any, Optional
from models.redemption import RedemptionType
from .catalog_service import RedemptionCatalogService

class ValueOptimizationService:
    def __init__(self, catalog_service: RedemptionCatalogService):
        self.catalog_service = catalog_service
        self._tier_bonuses = {
            "gold": 1.1,
            "platinum": 1.2,
            "diamond": 1.3
        }
    
    def analyze_redemption_values(self, member_tier: Optional[str] = None) -> List[Dict[str, Any]]:
        catalog = self.catalog_service.get_catalog(tier=member_tier, page_size=100)
        
        value_analysis = []
        for item in catalog["items"]:
            base_value_per_point = item["cash_value"] / item["points_required"]
            tier_bonus = self._tier_bonuses.get(member_tier, 1.0) if member_tier else 1.0
            effective_value = base_value_per_point * tier_bonus
            
            analysis = {
                "catalog_id": item["id"],
                "name": item["name"],
                "type": item["type"],
                "points_required": item["points_required"],
                "cash_value": item["cash_value"],
                "base_value_per_point": round(base_value_per_point, 4),
                "tier_bonus_multiplier": tier_bonus,
                "effective_value_per_point": round(effective_value, 4),
                "recommendation_score": self._calculate_recommendation_score(item, effective_value)
            }
            value_analysis.append(analysis)
        
        # Sort by effective value per point (descending)
        value_analysis.sort(key=lambda x: x["effective_value_per_point"], reverse=True)
        
        return value_analysis
    
    def get_best_value_recommendations(self, member_tier: Optional[str] = None, 
                                     available_points: float = 0, limit: int = 5) -> List[Dict[str, Any]]:
        analysis = self.analyze_redemption_values(member_tier)
        
        # Filter by available points
        if available_points > 0:
            analysis = [item for item in analysis if item["points_required"] <= available_points]
        
        recommendations = []
        for item in analysis[:limit]:
            recommendation = {
                **item,
                "recommendation_reason": self._get_recommendation_reason(item),
                "value_rating": self._get_value_rating(item["effective_value_per_point"])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def compare_redemption_options(self, catalog_ids: List[str], member_tier: Optional[str] = None) -> Dict[str, Any]:
        comparisons = []
        
        for catalog_id in catalog_ids:
            item_details = self.catalog_service.get_item_details(catalog_id)
            if not item_details:
                continue
            
            base_value_per_point = item_details["cash_value"] / item_details["points_required"]
            tier_bonus = self._tier_bonuses.get(member_tier, 1.0) if member_tier else 1.0
            effective_value = base_value_per_point * tier_bonus
            
            comparison = {
                "catalog_id": catalog_id,
                "name": item_details["name"],
                "type": item_details["type"],
                "points_required": item_details["points_required"],
                "cash_value": item_details["cash_value"],
                "value_per_point": round(effective_value, 4),
                "value_rating": self._get_value_rating(effective_value)
            }
            comparisons.append(comparison)
        
        # Sort by value per point
        comparisons.sort(key=lambda x: x["value_per_point"], reverse=True)
        
        best_option = comparisons[0] if comparisons else None
        
        return {
            "comparisons": comparisons,
            "best_option": best_option,
            "analysis_summary": {
                "total_options": len(comparisons),
                "value_range": {
                    "min": min(c["value_per_point"] for c in comparisons) if comparisons else 0,
                    "max": max(c["value_per_point"] for c in comparisons) if comparisons else 0
                }
            }
        }
    
    def get_personalized_recommendations(self, member_id: str, member_tier: Optional[str] = None,
                                       spending_patterns: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        base_recommendations = self.get_best_value_recommendations(member_tier)
        
        # Enhance with personalization
        for rec in base_recommendations:
            rec["personalization_score"] = self._calculate_personalization_score(
                rec, spending_patterns or {}
            )
        
        # Re-sort by combined recommendation and personalization score
        base_recommendations.sort(
            key=lambda x: (x["recommendation_score"] + x["personalization_score"]) / 2, 
            reverse=True
        )
        
        return base_recommendations
    
    def _calculate_recommendation_score(self, item: Dict[str, Any], effective_value: float) -> float:
        # Base score from value per point
        base_score = min(effective_value * 100, 100)  # Cap at 100
        
        # Bonus for travel and experiences (typically higher satisfaction)
        if item["type"] in [RedemptionType.TRAVEL, RedemptionType.EXPERIENCE]:
            base_score *= 1.1
        
        # Penalty for out of stock items
        if not item.get("in_stock", True):
            base_score *= 0.5
        
        return round(base_score, 2)
    
    def _calculate_personalization_score(self, item: Dict[str, Any], 
                                       spending_patterns: Dict[str, float]) -> float:
        # Simple personalization based on spending patterns
        item_type = item["type"]
        
        # If user spends a lot on travel, boost travel redemptions
        if item_type == RedemptionType.TRAVEL and spending_patterns.get("travel", 0) > 1000:
            return 20.0
        
        # If user prefers cashback, boost cashback options
        if item_type == RedemptionType.CASHBACK and spending_patterns.get("cashback_preference", 0) > 0.5:
            return 15.0
        
        return 0.0
    
    def _get_recommendation_reason(self, item: Dict[str, Any]) -> str:
        value_per_point = item["effective_value_per_point"]
        
        if value_per_point >= 0.015:
            return "Excellent value - among the best redemption rates"
        elif value_per_point >= 0.012:
            return "Good value - above average redemption rate"
        elif value_per_point >= 0.010:
            return "Fair value - standard redemption rate"
        else:
            return "Lower value - consider other options"
    
    def _get_value_rating(self, value_per_point: float) -> str:
        if value_per_point >= 0.015:
            return "Excellent"
        elif value_per_point >= 0.012:
            return "Good"
        elif value_per_point >= 0.010:
            return "Fair"
        else:
            return "Poor"