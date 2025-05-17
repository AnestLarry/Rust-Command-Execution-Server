from abc import ABC, abstractmethod
from typing import Any, List, Optional

class SQLDatabaseMethod(ABC):
    """Abstract base class for database methods."""

    @abstractmethod
    async def create(self, data: Any) -> Any:
        """Abstract method for creating data."""
        pass

    @abstractmethod
    async def read(self, query: Any) -> Optional[Any]:
        """Abstract method for reading data."""
        pass

    @abstractmethod
    async def delete(self, query: Any) -> bool:
        """Abstract method for deleting data."""
        pass
