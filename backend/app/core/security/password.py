"""Password hashing via passlib bcrypt."""

from __future__ import annotations

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, bcrypt__ident="2b",)


def hash_password(password: str) -> str:
    """Hash a password; never log or return the result to clients."""
    return pwd_context.hash(password)
