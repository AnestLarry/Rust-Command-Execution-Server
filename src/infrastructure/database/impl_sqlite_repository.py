from src.domain.db.repository.sql_repository import SQLDatabaseMethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Any, Optional, Dict, List


class SqliteRepository(SQLDatabaseMethod):
    """SQLite implementation of the DatabaseRepository abstract class."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, table_name: str, data: Dict[str, Any]) -> Any:
        """Concrete method for creating data in SQLite."""
        columns = ", ".join(data.keys())
        values = ", ".join([f":{key}" for key in data.keys()])
        query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        await self.session.execute(query, data)
        await self.session.commit()
        # For simplicity, returning the data back. In a real scenario, you might fetch the inserted row with its ID.
        return data

    async def read_single(self, table_name: str, query_filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Concrete method for reading a single data entry from SQLite."""
        conditions = " AND ".join([f"{key} = :{key}" for key in query_filter.keys()])
        query = text(f"SELECT * FROM {table_name} WHERE {conditions}")
        result = await self.session.execute(query, query_filter)
        row = result.first()
        if row:
            return dict(row)
        return None

    async def read_list(self, table_name: str, query_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Concrete method for reading a list of data entries from SQLite."""
        query_text = f"SELECT * FROM {table_name}"
        if query_filter:
            conditions = " AND ".join([f"{key} = :{key}" for key in query_filter.keys()])
            query_text += f" WHERE {conditions}"
            query = text(query_text)
            result = await self.session.execute(query, query_filter)
        else:
            query = text(query_text)
            result = await self.session.execute(query)

        rows = result.fetchall()
        return [dict(row) for row in rows]


    async def delete(self, table_name: str, query_filter: Dict[str, Any]) -> bool:
        """Concrete method for deleting data from SQLite."""
        conditions = " AND ".join([f"{key} = :{key}" for key in query_filter.keys()])
        query = text(f"DELETE FROM {table_name} WHERE {conditions}")
        result = await self.session.execute(query, query_filter)
        await self.session.commit()
        return result.rowcount > 0
