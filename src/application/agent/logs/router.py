from fastapi import APIRouter, Depends

from application.agent.logs.handler import LogsHandlerInterface

from ..dependencies import DependenciesFactory
from .dto import LogPayload

router = APIRouter()

@router.post("/logs")
async def upload_logs(
    payload: LogPayload,
    handler: LogsHandlerInterface = Depends(DependenciesFactory.get_logs_handler)
):
    """Upload execution logs from an agent."""
    return await handler.upload_logs(payload)
