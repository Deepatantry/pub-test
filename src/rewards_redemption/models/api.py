from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .category import Category, CategoryMultiplier, SpendingAnalytics
from .redemption import RedemptionCatalog, RedemptionTransaction, AutoRedemptionConfig

# Request Models
class ManualRedemptionRequest(BaseModel):
    member_id: str
    catalog_id: str
    quantity: int = 1

class AutoRedemptionConfigRequest(BaseModel):
    enabled: bool
    threshold_points: int
    redemption_type: str
    frequency: str = "immediate"

# Response Models
class CategoryResponse(BaseModel):
    categories: List[Category]
    multipliers: List[CategoryMultiplier]

class SpendingInsightsResponse(BaseModel):
    member_id: str
    analytics: List[SpendingAnalytics]
    recommendations: List[str]
    total_spending: float
    total_points: float

class RedemptionCatalogResponse(BaseModel):
    items: List[RedemptionCatalog]
    total_count: int
    page: int
    page_size: int

class ValueAnalysisResponse(BaseModel):
    catalog_id: str
    points_required: int
    cash_value: float
    value_per_point: float
    tier_bonus: Optional[float] = None
    recommendation: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()