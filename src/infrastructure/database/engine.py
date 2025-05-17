from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ...config import settings

def get_engine():
    """Create and return the appropriate database engine based on config."""
    if settings.DB_ENGINE == "postgres":
        return create_async_engine(
            settings.DB_URL,
            pool_pre_ping=True,
            echo=True
        )
    else:  # Default to SQLite
        return create_async_engine(
            settings.DB_URL,
            connect_args={"check_same_thread": False},
            echo=True
        )

async def get_session() -> AsyncSession:
    """Get an async database session."""
    engine = get_engine()
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session
