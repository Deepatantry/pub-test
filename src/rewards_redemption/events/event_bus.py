import asyncio
from typing import Dict, List, Callable, Any
from datetime import datetime
import json
from models.events import *

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_store: List[Dict[str, Any]] = []
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    async def publish(self, event_type: str, event_data: Any):
        # Store event
        event_record = {
            "id": len(self._event_store) + 1,
            "type": event_type,
            "data": event_data.dict() if hasattr(event_data, 'dict') else event_data,
            "timestamp": datetime.now(),
            "processed": False
        }
        self._event_store.append(event_record)
        
        # Notify subscribers
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    await asyncio.sleep(0.05)  # Simulate async processing
                    await handler(event_data)
                    event_record["processed"] = True
                except Exception as e:
                    print(f"Error processing event {event_type}: {e}")
    
    def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return sorted(self._event_store, key=lambda x: x["timestamp"], reverse=True)[:limit]

# Global event bus instance
event_bus = EventBus()