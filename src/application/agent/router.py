from fastapi import APIRouter

from .commands import router as commands_router
from .logs import router as logs_router

router = APIRouter(
    prefix="/api/v1", # Add a common prefix for all API groups
)

router.include_router(commands_router.router)
router.include_router(logs_router.router)
