from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.db.database import Base
from app.db import models  # noqa: F401  (needed for autogenerate)


# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config

# -------------------------------------------------
# Logging
# -------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# Metadata (for autogenerate)
# -------------------------------------------------
target_metadata = Base.metadata

# -------------------------------------------------
# Resolve DATABASE URL from environment
# -------------------------------------------------
DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Database URL not found. "
        "Set POSTGRES_URL or DATABASE_URL environment variable."
    )

# Inject resolved URL into Alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# -------------------------------------------------
# Offline migrations
# -------------------------------------------------
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with a URL only,
    without creating an Engine.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------
# Online migrations
# -------------------------------------------------
def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------
# Entrypoint
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
