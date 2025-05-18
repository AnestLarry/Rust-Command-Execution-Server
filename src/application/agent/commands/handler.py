from abc import ABC, abstractmethod
from datetime import datetime
from .dto import FetchTasksResponse, ServerTask # Import TaskDto
from domain.aggregate.agent.agent_repository import AgentRepository

class CommandsHandlerInterface(ABC):
    @abstractmethod
    async def fetch_commands(
        self,
        agent_id: str,
        since: datetime,
    ) -> FetchTasksResponse:
        pass

class CommandsHandler(CommandsHandlerInterface):
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def fetch_commands(
        self,
        agent_id: str,
        since: datetime,
    ) -> FetchTasksResponse:
        """Handler for fetching pending commands."""
        # Use the injected repository to get pending tasks
        tasks_data = await self.agent_repo.get_pending_tasks_for_agent(agent_id, since)

        # Convert task data to TaskDto (assuming task data is a dict matching TaskDto fields)
        tasks_dto = [ServerTask(**task) for task in tasks_data]

        return FetchTasksResponse(
            server_current_time=datetime.utcnow(),
            tasks=tasks_dto
        )
