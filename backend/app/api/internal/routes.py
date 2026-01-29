from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors.exceptions import DatabaseUnavailableError
from app.db.session import get_db


router = APIRouter()


@router.get("/healthz", summary="Internal health check")
async def healthz() -> dict[str, str]:
    """Simple internal health check endpoint."""
    return {"status": "ok"}


@router.get("/db-ping", summary="Internal DB ping")
async def db_ping(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise DatabaseUnavailableError() from exc

    return {"db": "ok"}

