from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RedemptionType(str, Enum):
    CASHBACK = "cashback"
    TRAVEL = "travel"
    MERCHANDISE = "merchandise"
    EXPERIENCE = "experience"

class RedemptionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class RedemptionCatalog(BaseModel):
    id: str
    name: str
    description: str
    type: RedemptionType
    points_required: int
    cash_value: float
    tier_exclusive: Optional[str] = None
    available: bool = True
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

class RedemptionInventory(BaseModel):
    id: str
    catalog_id: str
    stock_quantity: Optional[int] = None  # None for unlimited
    reserved_quantity: int = 0
    updated_at: datetime

class RedemptionTransaction(BaseModel):
    id: str
    member_id: str
    catalog_id: str
    points_used: int
    cash_value: float
    status: RedemptionStatus
    tracking_info: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime
    completed_at: Optional[datetime] = None

class AutoRedemptionConfig(BaseModel):
    id: str
    member_id: str
    enabled: bool
    threshold_points: int
    redemption_type: RedemptionType
    frequency: str  # "immediate", "monthly"
    created_at: datetime
    updated_at: datetime