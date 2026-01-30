"""
Application settings loaded from environment variables.

This module intentionally keeps configuration small.
Auth-related keys are placeholders only; never hardcode secrets.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Core application settings sourced from environment variables."""

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DOCS_ENABLED: bool = os.getenv("DOCS_ENABLED", "true").lower() in ("true", "1", "yes")

    # Auth / security placeholders (no auth implementation)
    AUTH_ACCESS_TOKEN_TTL_SECONDS: int = int(os.getenv("AUTH_ACCESS_TOKEN_TTL_SECONDS", "900"))
    AUTH_REFRESH_TOKEN_TTL_SECONDS: int = int(os.getenv("AUTH_REFRESH_TOKEN_TTL_SECONDS", "604800"))
    AUTH_TOKEN_SIGNING_KEY: str = os.getenv("AUTH_TOKEN_SIGNING_KEY", "")
    AUTH_TOKEN_ALG: str = os.getenv("AUTH_TOKEN_ALG", "HS256")
    EMAIL_VERIFY_TTL_SECONDS: int = int(os.getenv("EMAIL_VERIFY_TTL_SECONDS", "3600"))
    APP_PUBLIC_BASE_URL: str = os.getenv("APP_PUBLIC_BASE_URL", "http://localhost:8000")


settings = Settings()


