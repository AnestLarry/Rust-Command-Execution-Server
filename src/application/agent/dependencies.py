from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from domain.aggregate.agent.agent_repository import AgentRepository
from infrastructure.aggregate.agent.impl_agent_repository import AgentRepositoryImpl
from src.config import Settings, settings  # Import settings
from src.infrastructure.cloudflare_kv.impl_cloudflare_kv_repository import (
    CloudflareKVRepo,  # Assuming this is the KV repo
)
from src.infrastructure.database.engine import get_db
from src.infrastructure.database.impl_sqlite_repository import (
    SQLiteRepository,  # Assuming this is the SQLite repo
)

from .commands.handler import CommandsHandler, CommandsHandlerInterface
from .logs.handler import LogsHandler, LogsHandlerInterface


# Dependency to get the concrete repository implementation
def get_agent_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    # Assuming CloudflareKVRepo also has a dependency or can be instantiated directly
    # If CloudflareKVRepo needs dependencies, they should be injected here too
    kv_repo: CloudflareKVRepo = Depends(CloudflareKVRepo), # Adjust if KV repo needs dependencies
    app_settings: Settings = Depends(settings) # Inject settings
) -> AgentRepository:
    # Instantiate the specific repository implementations needed by AgentRepositoryImpl
    sqlite_repo = SQLiteRepository(db_session) # Assuming SQLiteRepository needs session
    # kv_repo is already instantiated by Depends

    return AgentRepositoryImpl(db_repo=sqlite_repo, kv_repo=kv_repo, settings=app_settings)


class DependenciesFactory:
    @staticmethod
    def get_commands_handler(
        agent_repo: Annotated[AgentRepository, Depends(get_agent_repository)]
    ) -> CommandsHandlerInterface:
        return CommandsHandler(agent_repo=agent_repo)

    @staticmethod
    def get_logs_handler(
        agent_repo: Annotated[AgentRepository, Depends(get_agent_repository)]
    ) -> LogsHandlerInterface:
        return LogsHandler(agent_repo=agent_repo)
