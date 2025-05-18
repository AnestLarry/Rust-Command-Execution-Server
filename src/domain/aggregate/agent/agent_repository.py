from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from ...db.repository.async_repository import AsyncRepository


class AgentRepository(AsyncRepository, ABC):
    @abstractmethod
    async def create_task(self, command: str, timeout: int, upload_log: bool) -> str:
        pass

    @abstractmethod
    async def get_task(self, task_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def store_log(
        self,
        task_id: str,
        agent_id: str,
        exit_code: int,
        stdout: str,
        stderr: str,
        exec_time_ms: int,
    ) -> None:
        pass

    @abstractmethod
    async def get_pending_tasks_for_agent(
        self, agent_id: str, since: datetime
    ) -> list[dict]:
        pass
