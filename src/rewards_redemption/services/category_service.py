from typing import List, Optional, Dict, Any
from datetime import datetime
from models.category import Category, CategoryMultiplier, CategoryStatus
from repositories.category_repository import CategoryRepository, CategoryMultiplierRepository

class CategoryManagementService:
    def __init__(self, category_repo: CategoryRepository, multiplier_repo: CategoryMultiplierRepository):
        self.category_repo = category_repo
        self.multiplier_repo = multiplier_repo
        self._cache: Dict[str, Any] = {}
    
    def get_active_categories(self) -> List[Category]:
        cache_key = "active_categories"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        categories = self.category_repo.get_active_categories()
        self._cache[cache_key] = categories
        return categories
    
    def get_category_with_multipliers(self, category_id: str, tier: Optional[str] = None) -> Dict[str, Any]:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            return {}
        
        multiplier = self.multiplier_repo.get_multiplier_for_tier(category_id, tier)
        
        return {
            "category": category,
            "multiplier": multiplier.multiplier if multiplier else 1.0,
            "spending_cap": category.spending_cap,
            "tier_specific": multiplier.tier is not None if multiplier else False
        }
    
    def create_category(self, name: str, description: str, spending_cap: Optional[float] = None) -> Category:
        category = Category(
            id=f"cat_{len(self.category_repo.get_all()) + 1}",
            name=name,
            description=description,
            status=CategoryStatus.ACTIVE,
            spending_cap=spending_cap,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._invalidate_cache()
        return self.category_repo.create(category)
    
    def update_category_multiplier(self, category_id: str, multiplier: float, tier: Optional[str] = None) -> CategoryMultiplier:
        # Deactivate existing multiplier
        existing = self.multiplier_repo.get_multiplier_for_tier(category_id, tier)
        if existing:
            existing.effective_to = datetime.now()
            self.multiplier_repo.update(existing.id, existing)
        
        # Create new multiplier
        new_multiplier = CategoryMultiplier(
            id=f"mult_{len(self.multiplier_repo.get_all()) + 1}",
            category_id=category_id,
            multiplier=multiplier,
            tier=tier,
            effective_from=datetime.now(),
            created_at=datetime.now()
        )
        self._invalidate_cache()
        return self.multiplier_repo.create(new_multiplier)
    
    def _invalidate_cache(self):
        self._cache.clear()