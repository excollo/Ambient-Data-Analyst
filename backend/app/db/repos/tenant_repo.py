"""Repository helpers for tenant persistence."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tenant import Tenant


async def get_tenant_by_slug(session: AsyncSession, slug: str) -> Optional[Tenant]:
    """Fetch a tenant by its slug, or None if it does not exist."""
    stmt = select(Tenant).where(Tenant.slug == slug)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

