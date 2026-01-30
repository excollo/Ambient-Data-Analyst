"""Repository helpers for user persistence."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def get_user_by_tenant_email(
    session: AsyncSession, tenant_id: str, email: str
) -> Optional[User]:
    """Fetch a user by tenant_id and email, or None if not found."""
    from uuid import UUID

    stmt = (
        select(User)
        .where(User.tenant_id == UUID(tenant_id))
        .where(User.email == email)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    *,
    tenant_id: str,
    email: str,
    password_hash: str,
) -> User:
    """Create a new user."""
    from uuid import UUID

    user = User(
        tenant_id=UUID(tenant_id),
        email=email,
        password_hash=password_hash,
    )
    session.add(user)
    await session.flush()
    return user
