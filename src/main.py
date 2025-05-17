from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.router import router as application_router  # Import the central router
from config import settings

app = FastAPI(
    title="Rust Command Execution Server",
    version="0.1.0",
    description="API server for managing agent commands and logs",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers

app.include_router(application_router.router)  # Include the central router


@app.on_event("startup")
async def startup():
    """Initialize application services."""
    pass


@app.on_event("shutdown")
async def shutdown():
    """Clean up resources."""
    pass
