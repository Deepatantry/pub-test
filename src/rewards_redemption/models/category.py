from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CategoryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SEASONAL = "seasonal"

class Category(BaseModel):
    id: str
    name: str
    description: str
    status: CategoryStatus
    spending_cap: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class CategoryMultiplier(BaseModel):
    id: str
    category_id: str
    multiplier: float
    tier: Optional[str] = None  # For tier-specific multipliers
    effective_from: datetime
    effective_to: Optional[datetime] = None
    created_at: datetime

class SpendingAnalytics(BaseModel):
    id: str
    member_id: str
    category_id: str
    period: str  # "monthly", "quarterly", "yearly"
    spending_amount: float
    points_earned: float
    transaction_count: int
    period_start: datetime
    period_end: datetime
    created_at: datetime