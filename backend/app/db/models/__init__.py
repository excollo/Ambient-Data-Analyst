"""Database models package."""

from __future__ import annotations

from app.db.models.tenant import Tenant
from app.db.models.user import User

__all__ = ["Tenant", "User"]

