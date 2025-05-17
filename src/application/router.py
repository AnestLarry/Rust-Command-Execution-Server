from fastapi import APIRouter

from .agent import router as agent_router

router = APIRouter(
    prefix="/api/v1", # Add a common prefix for all API groups
)

router.include_router(agent_router)
