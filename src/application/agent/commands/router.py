from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.engine import get_session
from .dto import FetchTasksResponse  # Import necessary DTO
from .handler import fetch_commands_handler  # Import handler

router = APIRouter()

@router.get("/commands", response_model=FetchTasksResponse)
async def fetch_commands(
    agent_id: str = Query(..., description="Agent identifier"),
    since: datetime = Query(None, description="Filter commands since this timestamp"),
    session: AsyncSession = Depends(get_session)
):
    """Fetch pending commands for the specified agent."""
    return await fetch_commands_handler(agent_id, since, session)
