from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

# Inbound Events
class TransactionProcessedEvent(BaseModel):
    transaction_id: str
    member_id: str
    amount: float
    category: str
    merchant: str
    timestamp: datetime
    points_earned: float

class PointsEarnedEvent(BaseModel):
    member_id: str
    points: float
    source: str
    transaction_id: Optional[str] = None
    timestamp: datetime

class BalanceUpdatedEvent(BaseModel):
    member_id: str
    new_balance: float
    change_amount: float
    reason: str
    timestamp: datetime

class TierAdvancedEvent(BaseModel):
    member_id: str
    old_tier: str
    new_tier: str
    timestamp: datetime

# Outbound Events
class CategoryUpdatedEvent(BaseModel):
    category_id: str
    action: str  # "created", "updated", "deactivated"
    changes: Dict[str, Any]
    timestamp: datetime

class RedemptionProcessedEvent(BaseModel):
    redemption_id: str
    member_id: str
    catalog_id: str
    points_used: int
    status: str
    timestamp: datetime

class AutoRedemptionTriggeredEvent(BaseModel):
    member_id: str
    redemption_id: str
    points_used: int
    trigger_reason: str
    timestamp: datetime

class SpendingInsightGeneratedEvent(BaseModel):
    member_id: str
    insights: Dict[str, Any]
    period: str
    timestamp: datetime