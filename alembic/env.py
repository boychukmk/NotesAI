import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

from database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Переменная окружения DATABASE_URL не установлена!")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    async with connectable.begin() as connection:
        await connection.run_sync(lambda conn: context.configure(
            connection=conn, target_metadata=target_metadata
        ))
        await connection.run_sync(lambda conn: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
