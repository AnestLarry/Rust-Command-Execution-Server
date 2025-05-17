from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.database.engine import get_session
from .dto import LogPayload # Import necessary DTO
from .handler import upload_logs_handler # Import handler

router = APIRouter()

@router.post("/logs")
async def upload_logs(
    payload: LogPayload,
    session: AsyncSession = Depends(get_session)
):
    """Upload execution logs from an agent."""
    return await upload_logs_handler(payload, session)
