"""
Alembic environment configuration.

Works inside Docker (cwd=/app) and supports offline/online migrations.
Reads DATABASE_URL from environment (fallback to sqlalchemy.url).
"""

from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.db.models import Tenant, User  # noqa: F401  # Ensure models are imported for metadata discovery
from app.db.base import Base

# Alembic Config object, providing access to values in alembic.ini.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support.
target_metadata = Base.metadata


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return config.get_main_option("sqlalchemy.url")


def _is_async_url(url: str) -> bool:
    # This repo uses asyncpg in DATABASE_URL (postgresql+asyncpg://...)
    return "+asyncpg" in url or url.startswith("postgresql+")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = _get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def _configure_and_run(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online_sync() -> None:
    """Run migrations in 'online' mode using a synchronous engine."""
    url = _get_database_url()
    config.set_main_option("sqlalchemy.url", url)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        _configure_and_run(connection)


async def run_migrations_online_async() -> None:
    """Run migrations in 'online' mode using an async engine."""
    url = _get_database_url()
    connectable: AsyncEngine = create_async_engine(url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(_configure_and_run)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    db_url = _get_database_url()
    if _is_async_url(db_url):
        asyncio.run(run_migrations_online_async())
    else:
        run_migrations_online_sync()
