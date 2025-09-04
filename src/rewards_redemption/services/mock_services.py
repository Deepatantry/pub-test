import asyncio
import random
from typing import Dict, Any
from config.settings import settings

class MockTravelPartnerAPI:
    async def book_travel(self, redemption_data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(settings.external_service_delay)
        
        # Simulate occasional failures
        if random.random() < 0.1:  # 10% failure rate
            return {"success": False, "error": "Travel partner service unavailable"}
        
        return {
            "success": True,
            "booking_id": f"TRV_{random.randint(100000, 999999)}",
            "confirmation_code": f"CONF{random.randint(1000, 9999)}",
            "estimated_delivery": "2-3 business days"
        }

class MockMerchandiseProvider:
    async def order_merchandise(self, redemption_data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(settings.external_service_delay)
        
        if random.random() < 0.05:  # 5% failure rate
            return {"success": False, "error": "Item temporarily out of stock"}
        
        return {
            "success": True,
            "order_id": f"MERCH_{random.randint(100000, 999999)}",
            "tracking_number": f"1Z{random.randint(100000000000, 999999999999)}",
            "estimated_delivery": "5-7 business days"
        }

class MockPaymentSystem:
    async def process_cashback(self, redemption_data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(settings.external_service_delay)
        
        if random.random() < 0.02:  # 2% failure rate
            return {"success": False, "error": "Payment processing error"}
        
        return {
            "success": True,
            "transaction_id": f"PAY_{random.randint(100000, 999999)}",
            "processing_time": "1-2 business days",
            "method": "statement_credit"
        }

class MockNotificationService:
    async def send_confirmation(self, member_id: str, message: str) -> Dict[str, Any]:
        await asyncio.sleep(0.01)  # Very fast for notifications
        
        return {
            "success": True,
            "notification_id": f"NOTIF_{random.randint(100000, 999999)}",
            "delivery_method": "email",
            "status": "sent"
        }

# Global instances
travel_api = MockTravelPartnerAPI()
merchandise_provider = MockMerchandiseProvider()
payment_system = MockPaymentSystem()
notification_service = MockNotificationService()