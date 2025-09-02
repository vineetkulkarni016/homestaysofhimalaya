import os
from alembic import context
from sqlalchemy import engine_from_config, pool

from services.booking.models import Base

config = context.config

target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./booking.db")


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": DATABASE_URL}, prefix="", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
