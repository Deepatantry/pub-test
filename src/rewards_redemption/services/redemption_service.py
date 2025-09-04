from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from models.redemption import RedemptionTransaction, RedemptionStatus, AutoRedemptionConfig, RedemptionType
from repositories.redemption_repository import RedemptionTransactionRepository, AutoRedemptionConfigRepository
from .catalog_service import RedemptionCatalogService

class RedemptionProcessingEngine:
    def __init__(self, transaction_repo: RedemptionTransactionRepository, 
                 config_repo: AutoRedemptionConfigRepository,
                 catalog_service: RedemptionCatalogService):
        self.transaction_repo = transaction_repo
        self.config_repo = config_repo
        self.catalog_service = catalog_service
        self._member_balances: Dict[str, float] = {}  # Mock point balances
    
    def process_manual_redemption(self, member_id: str, catalog_id: str, quantity: int = 1) -> Dict[str, Any]:
        # Validate catalog item
        item_details = self.catalog_service.get_item_details(catalog_id)
        if not item_details:
            return {"success": False, "error": "Item not found"}
        
        # Check availability
        availability = self.catalog_service.check_availability(catalog_id, quantity)
        if not availability["available"]:
            return {"success": False, "error": availability["reason"]}
        
        # Calculate total points needed
        total_points = item_details["points_required"] * quantity
        
        # Check member balance
        member_balance = self._get_member_balance(member_id)
        if member_balance < total_points:
            return {"success": False, "error": "Insufficient points"}
        
        # Reserve inventory
        if not self.catalog_service.reserve_inventory(catalog_id, quantity):
            return {"success": False, "error": "Could not reserve inventory"}
        
        # Create redemption transaction
        transaction = RedemptionTransaction(
            id=str(uuid.uuid4()),
            member_id=member_id,
            catalog_id=catalog_id,
            points_used=total_points,
            cash_value=item_details["cash_value"] * quantity,
            status=RedemptionStatus.PROCESSING,
            metadata={"quantity": quantity, "item_name": item_details["name"]},
            created_at=datetime.now()
        )
        
        # Deduct points and save transaction
        self._deduct_points(member_id, total_points)
        saved_transaction = self.transaction_repo.create(transaction)
        
        # Simulate processing completion
        self._complete_redemption(saved_transaction.id)
        
        return {
            "success": True,
            "transaction_id": saved_transaction.id,
            "points_used": total_points,
            "remaining_balance": self._get_member_balance(member_id)
        }
    
    def process_automatic_redemption(self, member_id: str) -> Optional[Dict[str, Any]]:
        config = self.config_repo.get_by_member(member_id)
        if not config or not config.enabled:
            return None
        
        member_balance = self._get_member_balance(member_id)
        if member_balance < config.threshold_points:
            return None
        
        # Find appropriate cashback option
        catalog = self.catalog_service.get_catalog(RedemptionType.CASHBACK)
        cashback_items = [item for item in catalog["items"] 
                         if item["points_required"] <= member_balance]
        
        if not cashback_items:
            return None
        
        # Select best value option
        best_item = max(cashback_items, key=lambda x: x["cash_value"] / x["points_required"])
        
        # Process redemption
        result = self.process_manual_redemption(member_id, best_item["id"])
        if result["success"]:
            result["auto_triggered"] = True
            result["trigger_reason"] = f"Balance exceeded {config.threshold_points} points"
        
        return result
    
    def get_redemption_history(self, member_id: str, limit: int = 50) -> Dict[str, Any]:
        transactions = self.transaction_repo.get_member_history(member_id, limit)
        
        enriched_transactions = []
        for transaction in transactions:
            item_details = self.catalog_service.get_item_details(transaction.catalog_id)
            enriched_transaction = {
                **transaction.dict(),
                "item_name": item_details["name"] if item_details else "Unknown Item",
                "item_type": item_details["type"] if item_details else "unknown"
            }
            enriched_transactions.append(enriched_transaction)
        
        return {
            "transactions": enriched_transactions,
            "total_count": len(transactions)
        }
    
    def _complete_redemption(self, transaction_id: str):
        transaction = self.transaction_repo.get_by_id(transaction_id)
        if transaction:
            transaction.status = RedemptionStatus.COMPLETED
            transaction.completed_at = datetime.now()
            transaction.tracking_info = f"TRACK_{transaction_id[:8].upper()}"
            self.transaction_repo.update(transaction_id, transaction)
    
    def _get_member_balance(self, member_id: str) -> float:
        return self._member_balances.get(member_id, 10000.0)  # Default mock balance
    
    def _deduct_points(self, member_id: str, points: float):
        current_balance = self._get_member_balance(member_id)
        self._member_balances[member_id] = current_balance - points
    
    def set_member_balance(self, member_id: str, balance: float):
        """Helper method for demo purposes"""
        self._member_balances[member_id] = balance