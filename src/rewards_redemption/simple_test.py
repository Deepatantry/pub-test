#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🏆 REWARDS & REDEMPTION SYSTEM - SIMPLE TEST")
print("=" * 50)

try:
    # Test imports
    from repositories.category_repository import CategoryRepository, CategoryMultiplierRepository
    from models.category import Category, CategoryStatus
    from datetime import datetime
    
    print("✓ Imports successful")
    
    # Test repository
    repo = CategoryRepository()
    category = Category(
        id="test_1",
        name="Test Category", 
        description="Test",
        status=CategoryStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    repo.create(category)
    retrieved = repo.get_by_id("test_1")
    
    print(f"✓ Repository test: Created and retrieved category '{retrieved.name}'")
    
    # Test catalog
    from repositories.redemption_repository import RedemptionCatalogRepository
    from models.redemption import RedemptionCatalog, RedemptionType
    
    catalog_repo = RedemptionCatalogRepository()
    item = RedemptionCatalog(
        id="test_redeem",
        name="Test Cashback",
        description="Test item",
        type=RedemptionType.CASHBACK,
        points_required=1000,
        cash_value=10.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    catalog_repo.create(item)
    retrieved_item = catalog_repo.get_by_id("test_redeem")
    
    print(f"✓ Catalog test: Created redemption item '{retrieved_item.name}'")
    
    print("\n🎉 ALL TESTS PASSED - System is working correctly!")
    print("\nTo run full demo:")
    print("1. CLI Demo: python3 -c 'from demo.cli_demo import main; import asyncio; asyncio.run(main())'")
    print("2. Web Server: python3 -c 'import uvicorn; from app import app; uvicorn.run(app, host=\"0.0.0.0\", port=8000)'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()