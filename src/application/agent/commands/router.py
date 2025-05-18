from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from ..dependencies import DependenciesFactory
from .dto import FetchTasksResponse
from .interfaces import CommandsHandlerInterface

router = APIRouter()

@router.get("/commands", response_model=FetchTasksResponse)
async def fetch_commands(
    agent_id: str = Query(..., description="Agent identifier"),
    since: datetime = Query(None, description="Filter commands since this timestamp"),
    handler: CommandsHandlerInterface = Depends(DependenciesFactory.get_commands_handler)
):
    """Fetch pending commands for the specified agent."""
    return await handler.fetch_commands(agent_id, since)
