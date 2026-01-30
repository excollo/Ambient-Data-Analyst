import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors.exceptions import DatabaseUnavailableError
from app.db.models.tenant import Tenant
from app.db.repos.tenant_repo import get_tenant_by_slug
from app.db.session import get_db


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/healthz", summary="Internal health check")
async def healthz() -> dict[str, str]:
    """Simple internal health check endpoint."""
    logger.info("Health check")
    return {"status": "ok"}


@router.get("/db-ping", summary="Internal DB ping")
async def db_ping(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise DatabaseUnavailableError() from exc

    return {"db": "ok"}


async def resolve_tenant(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    """Resolve the current tenant from the X-Tenant-ID header."""
    slug = request.headers.get("X-Tenant-ID")
    if not slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Tenant-ID header required",
        )

    tenant = await get_tenant_by_slug(db, slug=slug)
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    # Attach resolved tenant identifiers to the request state for downstream use.
    request.state.tenant_slug = tenant.slug  # type: ignore[attr-defined]
    request.state.tenant_id = str(tenant.id)  # type: ignore[attr-defined]

    return tenant


@router.get("/tenant", summary="Resolve current tenant")
async def get_current_tenant(
    request: Request,
    tenant: Tenant = Depends(resolve_tenant),
) -> dict[str, str]:
    """Return the resolved tenant identifiers from the request context."""
    # Values were set by resolve_tenant; fall back to model in case of state issues.
    tenant_slug: str = getattr(request.state, "tenant_slug", tenant.slug)  # type: ignore[attr-defined]
    tenant_id: str = getattr(request.state, "tenant_id", str(tenant.id))  # type: ignore[attr-defined]

    return {
        "tenant_slug": tenant_slug,
        "tenant_id": tenant_id,
    }

