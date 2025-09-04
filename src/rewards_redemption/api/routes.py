from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from models.api import *
from services.category_service import CategoryManagementService
from services.insights_service import SpendingInsightsEngine
from services.catalog_service import RedemptionCatalogService
from services.redemption_service import RedemptionProcessingEngine
from services.value_service import ValueOptimizationService

router = APIRouter()

# Dependency injection (will be properly set up in main.py)
category_service: CategoryManagementService = None
insights_service: SpendingInsightsEngine = None
catalog_service: RedemptionCatalogService = None
redemption_service: RedemptionProcessingEngine = None
value_service: ValueOptimizationService = None

@router.get("/categories/active")
async def get_active_categories():
    try:
        categories = category_service.get_active_categories()
        return ApiResponse(
            success=True,
            message="Active categories retrieved successfully",
            data={"categories": [cat.dict() for cat in categories]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/{member_id}/insights")
async def get_spending_insights(member_id: str, period: str = Query("monthly")):
    try:
        insights = insights_service.generate_insights(member_id, period)
        return ApiResponse(
            success=True,
            message="Spending insights generated successfully",
            data=insights
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/redemptions/catalog")
async def get_redemption_catalog(
    type: Optional[str] = None,
    tier: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    try:
        redemption_type = RedemptionType(type) if type else None
        catalog = catalog_service.get_catalog(redemption_type, tier, page, page_size)
        return ApiResponse(
            success=True,
            message="Redemption catalog retrieved successfully",
            data=catalog
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/redemptions/manual")
async def process_manual_redemption(request: ManualRedemptionRequest):
    try:
        result = redemption_service.process_manual_redemption(
            request.member_id, request.catalog_id, request.quantity
        )
        
        if result["success"]:
            return ApiResponse(
                success=True,
                message="Redemption processed successfully",
                data=result
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/redemptions/{member_id}/history")
async def get_redemption_history(member_id: str, limit: int = Query(50, ge=1, le=100)):
    try:
        history = redemption_service.get_redemption_history(member_id, limit)
        return ApiResponse(
            success=True,
            message="Redemption history retrieved successfully",
            data=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/redemptions/value-analysis")
async def get_value_analysis(member_tier: Optional[str] = None, available_points: float = Query(0)):
    try:
        analysis = value_service.analyze_redemption_values(member_tier)
        recommendations = value_service.get_best_value_recommendations(
            member_tier, available_points, limit=10
        )
        
        return ApiResponse(
            success=True,
            message="Value analysis completed successfully",
            data={
                "analysis": analysis[:20],  # Limit response size
                "recommendations": recommendations
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/{member_id}/recommendations")
async def get_category_recommendations(member_id: str):
    try:
        insights = insights_service.generate_insights(member_id)
        return ApiResponse(
            success=True,
            message="Category recommendations generated successfully",
            data={
                "member_id": member_id,
                "recommendations": insights.get("recommendations", []),
                "top_category": insights.get("top_category")
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))