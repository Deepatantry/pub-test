from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from repositories.category_repository import CategoryRepository, CategoryMultiplierRepository, SpendingAnalyticsRepository
from repositories.redemption_repository import *
from services.category_service import CategoryManagementService
from services.insights_service import SpendingInsightsEngine
from services.catalog_service import RedemptionCatalogService
from services.redemption_service import RedemptionProcessingEngine
from services.value_service import ValueOptimizationService
from events.handlers import EventHandlers
from api.routes import router
from demo.seed_data import *

# Initialize FastAPI app
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize repositories
category_repo = CategoryRepository()
multiplier_repo = CategoryMultiplierRepository()
analytics_repo = SpendingAnalyticsRepository()
catalog_repo = RedemptionCatalogRepository()
inventory_repo = RedemptionInventoryRepository()
transaction_repo = RedemptionTransactionRepository()
config_repo = AutoRedemptionConfigRepository()

# Initialize services
category_service = CategoryManagementService(category_repo, multiplier_repo)
insights_service = SpendingInsightsEngine(analytics_repo, category_repo)
catalog_service = RedemptionCatalogService(catalog_repo, inventory_repo)
redemption_service = RedemptionProcessingEngine(transaction_repo, config_repo, catalog_service)
value_service = ValueOptimizationService(catalog_service)

# Set up dependency injection for routes
import api.routes as routes_module
routes_module.category_service = category_service
routes_module.insights_service = insights_service
routes_module.catalog_service = catalog_service
routes_module.redemption_service = redemption_service
routes_module.value_service = value_service

# Initialize event handlers
event_handlers = EventHandlers(analytics_repo, redemption_service)

# Seed demo data
seed_categories(category_repo, multiplier_repo)
seed_redemption_catalog(catalog_repo, inventory_repo)
seed_sample_analytics(analytics_repo)
seed_auto_redemption_configs(config_repo)

# Set up member balances
redemption_service.set_member_balance("member1", 12000.0)
redemption_service.set_member_balance("member2", 8500.0)

# Include API routes
app.include_router(router)

@app.get("/")
async def serve_demo():
    return FileResponse("demo/templates/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.app_name}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)