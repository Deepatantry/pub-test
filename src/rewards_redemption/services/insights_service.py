from typing import List, Dict, Any
from datetime import datetime, timedelta
from models.category import SpendingAnalytics
from repositories.category_repository import SpendingAnalyticsRepository, CategoryRepository

class SpendingInsightsEngine:
    def __init__(self, analytics_repo: SpendingAnalyticsRepository, category_repo: CategoryRepository):
        self.analytics_repo = analytics_repo
        self.category_repo = category_repo
    
    def generate_insights(self, member_id: str, period: str = "monthly") -> Dict[str, Any]:
        analytics = self.analytics_repo.get_by_member_and_period(member_id, period)
        
        total_spending = sum(a.spending_amount for a in analytics)
        total_points = sum(a.points_earned for a in analytics)
        
        # Category breakdown
        category_breakdown = []
        for analytic in analytics:
            category = self.category_repo.get_by_id(analytic.category_id)
            category_breakdown.append({
                "category_name": category.name if category else "Unknown",
                "spending": analytic.spending_amount,
                "points": analytic.points_earned,
                "transactions": analytic.transaction_count,
                "avg_transaction": analytic.spending_amount / analytic.transaction_count if analytic.transaction_count > 0 else 0
            })
        
        # Sort by spending amount
        category_breakdown.sort(key=lambda x: x["spending"], reverse=True)
        
        recommendations = self._generate_recommendations(analytics)
        
        return {
            "member_id": member_id,
            "period": period,
            "total_spending": total_spending,
            "total_points": total_points,
            "category_breakdown": category_breakdown,
            "recommendations": recommendations,
            "top_category": category_breakdown[0]["category_name"] if category_breakdown else None
        }
    
    def calculate_category_utilization(self, member_id: str, category_id: str) -> Dict[str, Any]:
        analytics = self.analytics_repo.get_by_member_and_category(member_id, category_id)
        category = self.category_repo.get_by_id(category_id)
        
        if not analytics or not category:
            return {}
        
        current_month = [a for a in analytics if a.period == "monthly"][-1] if analytics else None
        
        utilization = 0.0
        if current_month and category.spending_cap:
            utilization = (current_month.spending_amount / category.spending_cap) * 100
        
        return {
            "category_name": category.name,
            "spending_cap": category.spending_cap,
            "current_spending": current_month.spending_amount if current_month else 0,
            "utilization_percentage": min(utilization, 100.0),
            "remaining_cap": max(0, (category.spending_cap or 0) - (current_month.spending_amount if current_month else 0))
        }
    
    def _generate_recommendations(self, analytics: List[SpendingAnalytics]) -> List[str]:
        recommendations = []
        
        if not analytics:
            return ["Start using your card to earn rewards!"]
        
        # Find underutilized categories
        categories = self.category_repo.get_active_categories()
        used_categories = {a.category_id for a in analytics}
        unused_categories = [c for c in categories if c.id not in used_categories]
        
        if unused_categories:
            recommendations.append(f"Consider using {unused_categories[0].name} category for bonus rewards")
        
        # Check for spending cap optimization
        for analytic in analytics:
            category = self.category_repo.get_by_id(analytic.category_id)
            if category and category.spending_cap:
                utilization = (analytic.spending_amount / category.spending_cap) * 100
                if utilization < 50:
                    recommendations.append(f"You're only using {utilization:.0f}% of your {category.name} bonus category")
                elif utilization > 90:
                    recommendations.append(f"You're close to maxing out {category.name} category this period")
        
        return recommendations[:3]  # Limit to top 3 recommendations