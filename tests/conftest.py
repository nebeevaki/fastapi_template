import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@pytest.fixture(scope="session")
def test_database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        pytest.fail(
            "DATABASE_URL is not set for tests",
            pytrace=False,
        )

    url = make_url(database_url)

    if (
        url.drivername != "postgresql+asyncpg"
        or url.database != "app_test_db"
        or url.username != "test"
        or url.host not in {"127.0.0.1", "localhost"}
    ):
        pytest.fail(
            "Tests must use the local app_test_db database",
            pytrace=False,
        )

    return database_url


@pytest_asyncio.fixture
async def test_session_factory(
    test_database_url: str,
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(test_database_url)

    try:
        async with engine.connect() as connection:
            transaction = await connection.begin()

            try:
                yield async_sessionmaker(
                    bind=connection,
                    expire_on_commit=False,
                    join_transaction_mode="create_savepoint",
                )
            finally:
                await transaction.rollback()
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def client(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncClient]:
    from app.db.session import get_session
    from app.main import app

    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as async_client:
            yield async_client
    finally:
        app.dependency_overrides.pop(get_session, None)
