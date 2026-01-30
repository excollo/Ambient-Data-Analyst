"""Repository helpers for tenant persistence."""

from __future__ import annotations

import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tenant import Tenant


async def get_tenant_by_slug(session: AsyncSession, slug: str) -> Optional[Tenant]:
    """Fetch a tenant by its slug, or None if it does not exist."""
    stmt = select(Tenant).where(Tenant.slug == slug)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_tenant_by_primary_domain(
    session: AsyncSession, domain: str
) -> Optional[Tenant]:
    """Fetch a tenant by primary_domain, or None if it does not exist."""
    stmt = select(Tenant).where(Tenant.primary_domain == domain)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def tenant_slug_exists(session: AsyncSession, slug: str) -> bool:
    """Check if a tenant with the given slug exists."""
    stmt = select(Tenant.id).where(Tenant.slug == slug).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def create_tenant(
    session: AsyncSession,
    *,
    slug: str,
    name: str,
    primary_domain: str,
) -> Tenant:
    """Create a new tenant. Caller must ensure slug uniqueness."""
    tenant = Tenant(slug=slug, name=name, primary_domain=primary_domain)
    session.add(tenant)
    await session.flush()
    return tenant

