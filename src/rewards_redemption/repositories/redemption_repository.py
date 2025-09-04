from typing import List, Optional
from .base import BaseRepository
from models.redemption import (
    RedemptionCatalog, RedemptionInventory, RedemptionTransaction, 
    AutoRedemptionConfig, RedemptionType, RedemptionStatus
)

class RedemptionCatalogRepository(BaseRepository[RedemptionCatalog]):
    def get_available_items(self) -> List[RedemptionCatalog]:
        return self.find_by(available=True)
    
    def get_by_type(self, redemption_type: RedemptionType) -> List[RedemptionCatalog]:
        return self.find_by(type=redemption_type)
    
    def get_by_tier(self, tier: Optional[str] = None) -> List[RedemptionCatalog]:
        if tier is None:
            return [item for item in self.get_all() if item.tier_exclusive is None]
        return self.find_by(tier_exclusive=tier)

class RedemptionInventoryRepository(BaseRepository[RedemptionInventory]):
    def get_by_catalog_id(self, catalog_id: str) -> Optional[RedemptionInventory]:
        results = self.find_by(catalog_id=catalog_id)
        return results[0] if results else None
    
    def is_available(self, catalog_id: str, quantity: int = 1) -> bool:
        inventory = self.get_by_catalog_id(catalog_id)
        if not inventory:
            return True  # Unlimited stock
        if inventory.stock_quantity is None:
            return True  # Unlimited stock
        available = inventory.stock_quantity - inventory.reserved_quantity
        return available >= quantity

class RedemptionTransactionRepository(BaseRepository[RedemptionTransaction]):
    def get_by_member(self, member_id: str) -> List[RedemptionTransaction]:
        return self.find_by(member_id=member_id)
    
    def get_by_status(self, status: RedemptionStatus) -> List[RedemptionTransaction]:
        return self.find_by(status=status)
    
    def get_member_history(self, member_id: str, limit: int = 50) -> List[RedemptionTransaction]:
        transactions = self.get_by_member(member_id)
        return sorted(transactions, key=lambda x: x.created_at, reverse=True)[:limit]

class AutoRedemptionConfigRepository(BaseRepository[AutoRedemptionConfig]):
    def get_by_member(self, member_id: str) -> Optional[AutoRedemptionConfig]:
        results = self.find_by(member_id=member_id)
        return results[0] if results else None
    
    def get_enabled_configs(self) -> List[AutoRedemptionConfig]:
        return self.find_by(enabled=True)