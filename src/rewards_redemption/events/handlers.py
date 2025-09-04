from datetime import datetime
from models.events import *
from models.category import SpendingAnalytics
from repositories.category_repository import SpendingAnalyticsRepository
from services.redemption_service import RedemptionProcessingEngine
from .event_bus import event_bus

class EventHandlers:
    def __init__(self, analytics_repo: SpendingAnalyticsRepository, 
                 redemption_service: RedemptionProcessingEngine):
        self.analytics_repo = analytics_repo
        self.redemption_service = redemption_service
        self._setup_handlers()
    
    def _setup_handlers(self):
        event_bus.subscribe("TransactionProcessedEvent", self.handle_transaction_processed)
        event_bus.subscribe("PointsEarnedEvent", self.handle_points_earned)
        event_bus.subscribe("BalanceUpdatedEvent", self.handle_balance_updated)
        event_bus.subscribe("TierAdvancedEvent", self.handle_tier_advanced)
    
    async def handle_transaction_processed(self, event: TransactionProcessedEvent):
        # Update spending analytics
        analytics_id = f"analytics_{event.member_id}_{event.category}_{datetime.now().strftime('%Y%m')}"
        
        existing = self.analytics_repo.get_by_id(analytics_id)
        if existing:
            existing.spending_amount += event.amount
            existing.points_earned += event.points_earned
            existing.transaction_count += 1
            self.analytics_repo.update(analytics_id, existing)
        else:
            analytics = SpendingAnalytics(
                id=analytics_id,
                member_id=event.member_id,
                category_id=event.category,
                period="monthly",
                spending_amount=event.amount,
                points_earned=event.points_earned,
                transaction_count=1,
                period_start=datetime.now().replace(day=1),
                period_end=datetime.now(),
                created_at=datetime.now()
            )
            self.analytics_repo.create(analytics)
        
        # Publish insights generated event
        await event_bus.publish("SpendingInsightGeneratedEvent", 
                               SpendingInsightGeneratedEvent(
                                   member_id=event.member_id,
                                   insights={"category": event.category, "amount": event.amount},
                                   period="monthly",
                                   timestamp=datetime.now()
                               ))
    
    async def handle_points_earned(self, event: PointsEarnedEvent):
        # Update member balance (mock)
        current_balance = self.redemption_service._get_member_balance(event.member_id)
        new_balance = current_balance + event.points
        self.redemption_service.set_member_balance(event.member_id, new_balance)
    
    async def handle_balance_updated(self, event: BalanceUpdatedEvent):
        # Check for auto-redemption triggers
        result = self.redemption_service.process_automatic_redemption(event.member_id)
        if result:
            await event_bus.publish("AutoRedemptionTriggeredEvent",
                                   AutoRedemptionTriggeredEvent(
                                       member_id=event.member_id,
                                       redemption_id=result["transaction_id"],
                                       points_used=result["points_used"],
                                       trigger_reason=result.get("trigger_reason", "Balance threshold reached"),
                                       timestamp=datetime.now()
                                   ))
    
    async def handle_tier_advanced(self, event: TierAdvancedEvent):
        # Tier advancement might unlock new redemption options
        print(f"Member {event.member_id} advanced from {event.old_tier} to {event.new_tier}")

# Event Publishers
class EventPublishers:
    @staticmethod
    async def publish_category_updated(category_id: str, action: str, changes: dict):
        await event_bus.publish("CategoryUpdatedEvent",
                               CategoryUpdatedEvent(
                                   category_id=category_id,
                                   action=action,
                                   changes=changes,
                                   timestamp=datetime.now()
                               ))
    
    @staticmethod
    async def publish_redemption_processed(redemption_id: str, member_id: str, 
                                         catalog_id: str, points_used: int, status: str):
        await event_bus.publish("RedemptionProcessedEvent",
                               RedemptionProcessedEvent(
                                   redemption_id=redemption_id,
                                   member_id=member_id,
                                   catalog_id=catalog_id,
                                   points_used=points_used,
                                   status=status,
                                   timestamp=datetime.now()
                               ))