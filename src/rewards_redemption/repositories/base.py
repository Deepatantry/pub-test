from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(ABC, Generic[T]):
    def __init__(self):
        self._data: Dict[str, T] = {}
    
    def create(self, entity: T) -> T:
        self._data[entity.id] = entity
        return entity
    
    def get_by_id(self, id: str) -> Optional[T]:
        return self._data.get(id)
    
    def get_all(self) -> List[T]:
        return list(self._data.values())
    
    def update(self, id: str, entity: T) -> Optional[T]:
        if id in self._data:
            self._data[id] = entity
            return entity
        return None
    
    def delete(self, id: str) -> bool:
        if id in self._data:
            del self._data[id]
            return True
        return False
    
    def find_by(self, **kwargs) -> List[T]:
        results = []
        for entity in self._data.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(entity, key) or getattr(entity, key) != value:
                    match = False
                    break
            if match:
                results.append(entity)
        return results