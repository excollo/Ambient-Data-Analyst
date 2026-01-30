"""Auth service: signup and future login/verification logic."""

from __future__ import annotations

import secrets
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors.exceptions import BadRequestError
from app.core.security.password import hash_password
from app.db.models.tenant import Tenant
from app.db.repos.tenant_repo import (
    create_tenant,
    get_tenant_by_primary_domain,
    tenant_slug_exists,
)
from app.db.repos.user_repo import create_user, get_user_by_tenant_email

PUBLIC_EMAIL_DOMAINS = frozenset([
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "icloud.com",
    "proton.me",
    "protonmail.com",
])


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _extract_domain(email: str) -> str:
    parts = email.split("@")
    if len(parts) != 2:
        raise BadRequestError("Invalid email format")
    return parts[1].lower()


def _make_tenant_slug(domain: str) -> str:
    return "t_" + domain.replace(".", "_")


async def signup(
    session: AsyncSession,
    *,
    email: str,
    password: str,
) -> None:
    """
    Signup: create tenant if new domain, add user to tenant.
    Returns None on success. Raises BadRequestError for public domains.
    Same response for new user or existing user (no enumeration).
    """
    normalized_email = _normalize_email(email)
    domain = _extract_domain(normalized_email)

    if domain in PUBLIC_EMAIL_DOMAINS:
        raise BadRequestError("Please use your work email address.")

    tenant = await get_tenant_by_primary_domain(session, domain)

    if tenant is None:
        base_slug = _make_tenant_slug(domain)
        slug = base_slug
        while await tenant_slug_exists(session, slug):
            suffix = secrets.token_hex(3)
            slug = f"{base_slug}_{suffix}"

        tenant = await create_tenant(
            session,
            slug=slug,
            name=domain,
            primary_domain=domain,
        )

    existing_user = await get_user_by_tenant_email(
        session, str(tenant.id), normalized_email
    )
    if existing_user is not None:
        return

    password_hash = hash_password(password)
    await create_user(
        session,
        tenant_id=str(tenant.id),
        email=normalized_email,
        password_hash=password_hash,
    )
