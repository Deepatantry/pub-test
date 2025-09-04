from datetime import datetime, timedelta
from models.category import Category, CategoryMultiplier, SpendingAnalytics, CategoryStatus
from models.redemption import RedemptionCatalog, RedemptionInventory, RedemptionType, AutoRedemptionConfig

def seed_categories(category_repo, multiplier_repo):
    categories = [
        Category(
            id="cat_1", name="Dining", description="Restaurants and food delivery",
            status=CategoryStatus.ACTIVE, spending_cap=1500.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        Category(
            id="cat_2", name="Gas Stations", description="Fuel and automotive",
            status=CategoryStatus.ACTIVE, spending_cap=1000.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        Category(
            id="cat_3", name="Grocery", description="Supermarkets and grocery stores",
            status=CategoryStatus.ACTIVE, spending_cap=2000.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        Category(
            id="cat_4", name="Travel", description="Airlines, hotels, and travel",
            status=CategoryStatus.SEASONAL, spending_cap=3000.0,
            start_date=datetime.now(), end_date=datetime.now() + timedelta(days=90),
            created_at=datetime.now(), updated_at=datetime.now()
        )
    ]
    
    multipliers = [
        CategoryMultiplier(
            id="mult_1", category_id="cat_1", multiplier=3.0, tier=None,
            effective_from=datetime.now(), created_at=datetime.now()
        ),
        CategoryMultiplier(
            id="mult_2", category_id="cat_2", multiplier=2.0, tier=None,
            effective_from=datetime.now(), created_at=datetime.now()
        ),
        CategoryMultiplier(
            id="mult_3", category_id="cat_3", multiplier=2.5, tier=None,
            effective_from=datetime.now(), created_at=datetime.now()
        ),
        CategoryMultiplier(
            id="mult_4", category_id="cat_4", multiplier=5.0, tier=None,
            effective_from=datetime.now(), created_at=datetime.now()
        ),
        # Tier-specific multipliers
        CategoryMultiplier(
            id="mult_5", category_id="cat_1", multiplier=4.0, tier="gold",
            effective_from=datetime.now(), created_at=datetime.now()
        )
    ]
    
    for category in categories:
        category_repo.create(category)
    
    for multiplier in multipliers:
        multiplier_repo.create(multiplier)

def seed_redemption_catalog(catalog_repo, inventory_repo):
    catalog_items = [
        RedemptionCatalog(
            id="redeem_1", name="Statement Credit $25", description="$25 statement credit",
            type=RedemptionType.CASHBACK, points_required=2500, cash_value=25.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        RedemptionCatalog(
            id="redeem_2", name="Statement Credit $50", description="$50 statement credit",
            type=RedemptionType.CASHBACK, points_required=5000, cash_value=50.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        RedemptionCatalog(
            id="redeem_3", name="Flight Credit $200", description="Airline credit for flights",
            type=RedemptionType.TRAVEL, points_required=15000, cash_value=200.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        RedemptionCatalog(
            id="redeem_4", name="Hotel Night", description="One night hotel stay",
            type=RedemptionType.TRAVEL, points_required=12000, cash_value=150.0,
            tier_exclusive="gold", created_at=datetime.now(), updated_at=datetime.now()
        ),
        RedemptionCatalog(
            id="redeem_5", name="Wireless Headphones", description="Premium wireless headphones",
            type=RedemptionType.MERCHANDISE, points_required=8000, cash_value=100.0,
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        RedemptionCatalog(
            id="redeem_6", name="Concert Tickets", description="Premium concert experience",
            type=RedemptionType.EXPERIENCE, points_required=20000, cash_value=250.0,
            tier_exclusive="platinum", created_at=datetime.now(), updated_at=datetime.now()
        )
    ]
    
    inventory_items = [
        RedemptionInventory(id="inv_1", catalog_id="redeem_1", stock_quantity=None, reserved_quantity=0, updated_at=datetime.now()),
        RedemptionInventory(id="inv_2", catalog_id="redeem_2", stock_quantity=None, reserved_quantity=0, updated_at=datetime.now()),
        RedemptionInventory(id="inv_3", catalog_id="redeem_3", stock_quantity=100, reserved_quantity=5, updated_at=datetime.now()),
        RedemptionInventory(id="inv_4", catalog_id="redeem_4", stock_quantity=50, reserved_quantity=2, updated_at=datetime.now()),
        RedemptionInventory(id="inv_5", catalog_id="redeem_5", stock_quantity=25, reserved_quantity=1, updated_at=datetime.now()),
        RedemptionInventory(id="inv_6", catalog_id="redeem_6", stock_quantity=10, reserved_quantity=0, updated_at=datetime.now())
    ]
    
    for item in catalog_items:
        catalog_repo.create(item)
    
    for inventory in inventory_items:
        inventory_repo.create(inventory)

def seed_sample_analytics(analytics_repo):
    sample_analytics = [
        SpendingAnalytics(
            id="analytics_member1_cat_1_202412", member_id="member1", category_id="cat_1",
            period="monthly", spending_amount=850.0, points_earned=2550.0, transaction_count=15,
            period_start=datetime.now().replace(day=1), period_end=datetime.now(),
            created_at=datetime.now()
        ),
        SpendingAnalytics(
            id="analytics_member1_cat_2_202412", member_id="member1", category_id="cat_2",
            period="monthly", spending_amount=320.0, points_earned=640.0, transaction_count=8,
            period_start=datetime.now().replace(day=1), period_end=datetime.now(),
            created_at=datetime.now()
        ),
        SpendingAnalytics(
            id="analytics_member2_cat_3_202412", member_id="member2", category_id="cat_3",
            period="monthly", spending_amount=1200.0, points_earned=3000.0, transaction_count=12,
            period_start=datetime.now().replace(day=1), period_end=datetime.now(),
            created_at=datetime.now()
        )
    ]
    
    for analytics in sample_analytics:
        analytics_repo.create(analytics)

def seed_auto_redemption_configs(config_repo):
    configs = [
        AutoRedemptionConfig(
            id="config_1", member_id="member1", enabled=True, threshold_points=5000,
            redemption_type=RedemptionType.CASHBACK, frequency="immediate",
            created_at=datetime.now(), updated_at=datetime.now()
        ),
        AutoRedemptionConfig(
            id="config_2", member_id="member2", enabled=False, threshold_points=10000,
            redemption_type=RedemptionType.CASHBACK, frequency="monthly",
            created_at=datetime.now(), updated_at=datetime.now()
        )
    ]
    
    for config in configs:
        config_repo.create(config)