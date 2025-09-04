from typing import List, Optional
from .base import BaseRepository
from models.category import Category, CategoryMultiplier, SpendingAnalytics, CategoryStatus

class CategoryRepository(BaseRepository[Category]):
    def get_active_categories(self) -> List[Category]:
        return self.find_by(status=CategoryStatus.ACTIVE)
    
    def get_by_name(self, name: str) -> Optional[Category]:
        results = self.find_by(name=name)
        return results[0] if results else None

class CategoryMultiplierRepository(BaseRepository[CategoryMultiplier]):
    def get_active_multipliers(self, category_id: str) -> List[CategoryMultiplier]:
        from datetime import datetime
        now = datetime.now()
        multipliers = self.find_by(category_id=category_id)
        return [m for m in multipliers if m.effective_from <= now and (m.effective_to is None or m.effective_to > now)]
    
    def get_multiplier_for_tier(self, category_id: str, tier: Optional[str] = None) -> Optional[CategoryMultiplier]:
        multipliers = self.get_active_multipliers(category_id)
        for m in multipliers:
            if m.tier == tier:
                return m
        # Fallback to default multiplier (tier=None)
        for m in multipliers:
            if m.tier is None:
                return m
        return None

class SpendingAnalyticsRepository(BaseRepository[SpendingAnalytics]):
    def get_by_member_and_period(self, member_id: str, period: str) -> List[SpendingAnalytics]:
        return self.find_by(member_id=member_id, period=period)
    
    def get_by_member_and_category(self, member_id: str, category_id: str) -> List[SpendingAnalytics]:
        return self.find_by(member_id=member_id, category_id=category_id)