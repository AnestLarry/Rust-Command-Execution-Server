from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict

class NoSqlRepository(ABC):
    """Abstract base class for NoSQL database methods."""

    @abstractmethod
    async def create(self, key: str, value: Any) -> None:
        """Abstract method for creating data (key-value pair)."""
        pass

    @abstractmethod
    async def read_single(self, key: str) -> Optional[Any]:
        """Abstract method for reading a single value by key."""
        pass

    @abstractmethod
    async def read_list(self, prefix: str) -> List[Dict[str, Any]]:
        """Abstract method for reading a list of values by prefix."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Abstract method for deleting data by key."""
        pass
