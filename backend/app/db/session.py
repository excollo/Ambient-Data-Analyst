"""
Database session management.

Foundation-only async SQLAlchemy plumbing:
- async engine from settings.DATABASE_URL
- async session maker
- FastAPI dependency to yield a session and close it
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config.settings import settings


engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
