from typing import List, Optional, Dict, Any
from models.redemption import RedemptionCatalog, RedemptionInventory, RedemptionType
from repositories.redemption_repository import RedemptionCatalogRepository, RedemptionInventoryRepository

class RedemptionCatalogService:
    def __init__(self, catalog_repo: RedemptionCatalogRepository, inventory_repo: RedemptionInventoryRepository):
        self.catalog_repo = catalog_repo
        self.inventory_repo = inventory_repo
        self._cache: Dict[str, Any] = {}
    
    def get_catalog(self, redemption_type: Optional[RedemptionType] = None, tier: Optional[str] = None, 
                   page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        cache_key = f"catalog_{redemption_type}_{tier}_{page}_{page_size}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Get available items
        items = self.catalog_repo.get_available_items()
        
        # Filter by type
        if redemption_type:
            items = [item for item in items if item.type == redemption_type]
        
        # Filter by tier
        if tier:
            items = [item for item in items if item.tier_exclusive is None or item.tier_exclusive == tier]
        else:
            items = [item for item in items if item.tier_exclusive is None]
        
        # Add inventory information
        enriched_items = []
        for item in items:
            inventory = self.inventory_repo.get_by_catalog_id(item.id)
            enriched_item = {
                **item.dict(),
                "in_stock": self.inventory_repo.is_available(item.id),
                "stock_quantity": inventory.stock_quantity if inventory else None
            }
            enriched_items.append(enriched_item)
        
        # Pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_items = enriched_items[start_idx:end_idx]
        
        result = {
            "items": paginated_items,
            "total_count": len(enriched_items),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(enriched_items) + page_size - 1) // page_size
        }
        
        self._cache[cache_key] = result
        return result
    
    def get_item_details(self, catalog_id: str) -> Optional[Dict[str, Any]]:
        item = self.catalog_repo.get_by_id(catalog_id)
        if not item:
            return None
        
        inventory = self.inventory_repo.get_by_catalog_id(catalog_id)
        
        return {
            **item.dict(),
            "in_stock": self.inventory_repo.is_available(catalog_id),
            "stock_quantity": inventory.stock_quantity if inventory else None,
            "reserved_quantity": inventory.reserved_quantity if inventory else 0
        }
    
    def check_availability(self, catalog_id: str, quantity: int = 1) -> Dict[str, Any]:
        item = self.catalog_repo.get_by_id(catalog_id)
        if not item or not item.available:
            return {"available": False, "reason": "Item not available"}
        
        if not self.inventory_repo.is_available(catalog_id, quantity):
            return {"available": False, "reason": "Insufficient stock"}
        
        return {"available": True, "reason": "Available"}
    
    def reserve_inventory(self, catalog_id: str, quantity: int = 1) -> bool:
        if not self.inventory_repo.is_available(catalog_id, quantity):
            return False
        
        inventory = self.inventory_repo.get_by_catalog_id(catalog_id)
        if inventory:
            inventory.reserved_quantity += quantity
            self.inventory_repo.update(inventory.id, inventory)
        
        self._invalidate_cache()
        return True
    
    def release_inventory(self, catalog_id: str, quantity: int = 1) -> bool:
        inventory = self.inventory_repo.get_by_catalog_id(catalog_id)
        if inventory and inventory.reserved_quantity >= quantity:
            inventory.reserved_quantity -= quantity
            self.inventory_repo.update(inventory.id, inventory)
            self._invalidate_cache()
            return True
        return False
    
    def _invalidate_cache(self):
        self._cache.clear()