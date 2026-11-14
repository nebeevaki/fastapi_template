import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

import app.db.models  # noqa: F401
from app.core.config import settings
from app.db.base import Base

# Alembic Config содержит настройки из alembic.ini.
config = context.config

# Используем стандартную конфигурацию логирования Alembic.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные всех зарегистрированных ORM-моделей.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Генерация SQL без подключения к базе данных."""
    # конфигурация среды исполнения миграции
    context.configure(
        url=str(settings.database_url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Выполнение миграций через синхронный интерфейс Alembic."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=False,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Создание async engine и выполнение миграций."""

    connectable = create_async_engine(
        str(settings.database_url),
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск асинхронной миграционной среды."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
