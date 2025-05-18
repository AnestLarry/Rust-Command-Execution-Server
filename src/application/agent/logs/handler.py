from abc import ABC, abstractmethod
from .dto import LogPayload
from domain.aggregate.agent.agent_repository import AgentRepository

class LogsHandlerInterface(ABC):
    @abstractmethod
    async def upload_logs(
        self,
        payload: LogPayload,
    ) -> None:
        pass

class LogsHandler(LogsHandlerInterface):
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def upload_logs(
        self,
        payload: LogPayload,
    ) -> None:
        """Handler for uploading execution logs."""
        # Use the injected repository to store the log
        await self.agent_repo.store_log(
            task_id=payload.task_id,
            agent_id=payload.agent_id,
            exit_code=payload.exit_code,
            stdout=payload.stdout,
            stderr=payload.stderr,
            exec_time_ms=payload.execution_time_ms
        )
