"""Seed script for initial tenants."""

from __future__ import annotations

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tenant import Tenant
from app.db.session import AsyncSessionLocal


async def _seed_tenants_once(session: AsyncSession) -> None:
    """Idempotently ensure the demo tenant exists."""
    slug = "t_demo"

    result = await session.execute(select(Tenant).where(Tenant.slug == slug))
    existing = result.scalar_one_or_none()
    if existing is not None:
        return

    tenant = Tenant(slug=slug, name="Demo Tenant")
    session.add(tenant)
    await session.commit()


async def seed_tenants() -> None:
    async with AsyncSessionLocal() as session:  # type: ignore[call-arg]
        await _seed_tenants_once(session)


def main() -> None:
    asyncio.run(seed_tenants())


if __name__ == "__main__":
    main()

