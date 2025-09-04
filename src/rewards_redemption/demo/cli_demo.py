import asyncio
import json
from datetime import datetime
from repositories.category_repository import CategoryRepository, CategoryMultiplierRepository, SpendingAnalyticsRepository
from repositories.redemption_repository import *
from services.category_service import CategoryManagementService
from services.insights_service import SpendingInsightsEngine
from services.catalog_service import RedemptionCatalogService
from services.redemption_service import RedemptionProcessingEngine
from services.value_service import ValueOptimizationService
from events.handlers import EventHandlers
from events.event_bus import event_bus
from models.events import TransactionProcessedEvent, PointsEarnedEvent
from .seed_data import *

class RewardsRedemptionDemo:
    def __init__(self):
        self._setup_repositories()
        self._setup_services()
        self._seed_data()
        self._setup_event_handlers()
    
    def _setup_repositories(self):
        self.category_repo = CategoryRepository()
        self.multiplier_repo = CategoryMultiplierRepository()
        self.analytics_repo = SpendingAnalyticsRepository()
        self.catalog_repo = RedemptionCatalogRepository()
        self.inventory_repo = RedemptionInventoryRepository()
        self.transaction_repo = RedemptionTransactionRepository()
        self.config_repo = AutoRedemptionConfigRepository()
    
    def _setup_services(self):
        self.category_service = CategoryManagementService(self.category_repo, self.multiplier_repo)
        self.insights_service = SpendingInsightsEngine(self.analytics_repo, self.category_repo)
        self.catalog_service = RedemptionCatalogService(self.catalog_repo, self.inventory_repo)
        self.redemption_service = RedemptionProcessingEngine(
            self.transaction_repo, self.config_repo, self.catalog_service
        )
        self.value_service = ValueOptimizationService(self.catalog_service)
    
    def _seed_data(self):
        seed_categories(self.category_repo, self.multiplier_repo)
        seed_redemption_catalog(self.catalog_repo, self.inventory_repo)
        seed_sample_analytics(self.analytics_repo)
        seed_auto_redemption_configs(self.config_repo)
        
        # Set up member balances
        self.redemption_service.set_member_balance("member1", 12000.0)
        self.redemption_service.set_member_balance("member2", 8500.0)
    
    def _setup_event_handlers(self):
        self.event_handlers = EventHandlers(self.analytics_repo, self.redemption_service)
    
    async def run_demo(self):
        while True:
            print("\n" + "="*50)
            print("REWARDS & REDEMPTION SYSTEM DEMO")
            print("="*50)
            print("1. View Active Categories")
            print("2. View Spending Insights")
            print("3. Browse Redemption Catalog")
            print("4. Process Manual Redemption")
            print("5. View Redemption History")
            print("6. Get Value Analysis")
            print("7. Simulate Transaction Event")
            print("8. View Event History")
            print("9. Exit")
            
            choice = input("\nSelect an option (1-9): ").strip()
            
            try:
                if choice == "1":
                    await self._demo_categories()
                elif choice == "2":
                    await self._demo_insights()
                elif choice == "3":
                    await self._demo_catalog()
                elif choice == "4":
                    await self._demo_redemption()
                elif choice == "5":
                    await self._demo_history()
                elif choice == "6":
                    await self._demo_value_analysis()
                elif choice == "7":
                    await self._demo_transaction_event()
                elif choice == "8":
                    await self._demo_event_history()
                elif choice == "9":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
            
            input("\nPress Enter to continue...")
    
    async def _demo_categories(self):
        print("\n--- ACTIVE CATEGORIES ---")
        categories = self.category_service.get_active_categories()
        for cat in categories:
            multiplier_info = self.category_service.get_category_with_multipliers(cat.id)
            print(f"• {cat.name}: {multiplier_info['multiplier']}x points")
            print(f"  Cap: ${cat.spending_cap or 'No limit'}")
            print(f"  Status: {cat.status}")
    
    async def _demo_insights(self):
        member_id = input("Enter member ID (member1/member2): ").strip() or "member1"
        print(f"\n--- SPENDING INSIGHTS FOR {member_id.upper()} ---")
        
        insights = self.insights_service.generate_insights(member_id)
        print(f"Total Spending: ${insights['total_spending']:.2f}")
        print(f"Total Points: {insights['total_points']:.0f}")
        print(f"Top Category: {insights['top_category'] or 'None'}")
        
        print("\nCategory Breakdown:")
        for cat in insights['category_breakdown']:
            print(f"• {cat['category_name']}: ${cat['spending']:.2f} → {cat['points']:.0f} pts")
        
        print("\nRecommendations:")
        for rec in insights['recommendations']:
            print(f"• {rec}")
    
    async def _demo_catalog(self):
        print("\n--- REDEMPTION CATALOG ---")
        catalog = self.catalog_service.get_catalog(page_size=10)
        
        for item in catalog['items']:
            stock_status = "✓ In Stock" if item['in_stock'] else "✗ Out of Stock"
            print(f"• {item['name']} ({item['type']})")
            print(f"  Points: {item['points_required']:,} | Value: ${item['cash_value']:.2f} | {stock_status}")
    
    async def _demo_redemption(self):
        member_id = input("Enter member ID (member1/member2): ").strip() or "member1"
        catalog_id = input("Enter catalog ID (redeem_1 to redeem_6): ").strip() or "redeem_1"
        
        balance = self.redemption_service._get_member_balance(member_id)
        print(f"\nCurrent balance: {balance:.0f} points")
        
        result = self.redemption_service.process_manual_redemption(member_id, catalog_id)
        
        if result['success']:
            print(f"✓ Redemption successful!")
            print(f"Transaction ID: {result['transaction_id']}")
            print(f"Points used: {result['points_used']}")
            print(f"Remaining balance: {result['remaining_balance']:.0f}")
        else:
            print(f"✗ Redemption failed: {result['error']}")
    
    async def _demo_history(self):
        member_id = input("Enter member ID (member1/member2): ").strip() or "member1"
        print(f"\n--- REDEMPTION HISTORY FOR {member_id.upper()} ---")
        
        history = self.redemption_service.get_redemption_history(member_id)
        
        if not history['transactions']:
            print("No redemption history found.")
            return
        
        for txn in history['transactions'][:5]:  # Show last 5
            print(f"• {txn['item_name']} - {txn['status']}")
            print(f"  Points: {txn['points_used']:,} | Date: {txn['created_at'].strftime('%Y-%m-%d %H:%M')}")
    
    async def _demo_value_analysis(self):
        tier = input("Enter member tier (gold/platinum/diamond or press Enter): ").strip() or None
        print(f"\n--- VALUE ANALYSIS {f'FOR {tier.upper()} TIER' if tier else ''} ---")
        
        recommendations = self.value_service.get_best_value_recommendations(tier, limit=5)
        
        for rec in recommendations:
            print(f"• {rec['name']} ({rec['type']})")
            print(f"  Value: {rec['effective_value_per_point']:.4f} $/point | Rating: {rec['value_rating']}")
            print(f"  {rec['recommendation_reason']}")
    
    async def _demo_transaction_event(self):
        member_id = input("Enter member ID (member1/member2): ").strip() or "member1"
        amount = float(input("Enter transaction amount ($): ").strip() or "100")
        category = input("Enter category (cat_1 to cat_4): ").strip() or "cat_1"
        
        # Simulate transaction event
        event = TransactionProcessedEvent(
            transaction_id=f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            member_id=member_id,
            amount=amount,
            category=category,
            merchant="Demo Merchant",
            timestamp=datetime.now(),
            points_earned=amount * 2.0  # Simplified calculation
        )
        
        await event_bus.publish("TransactionProcessedEvent", event)
        print(f"✓ Transaction event published: ${amount} at {category}")
    
    async def _demo_event_history(self):
        print("\n--- EVENT HISTORY ---")
        events = event_bus.get_event_history(10)
        
        for event in events:
            status = "✓" if event['processed'] else "⏳"
            print(f"{status} {event['type']} - {event['timestamp'].strftime('%H:%M:%S')}")

async def main():
    demo = RewardsRedemptionDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())