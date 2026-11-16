import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.users.models import User


@pytest.mark.asyncio
async def test_get_users_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_users_returns_users(
    client: AsyncClient,
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with test_session_factory() as session:
        session.add_all(
            [
                User(name="Анна"),
                User(name="Борис"),
            ]
        )
        await session.commit()

    response = await client.get("/api/v1/users")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert [user["name"] for user in data] == ["Анна", "Борис"]

    assert all(set(user) == {"id", "name"} for user in data)

    assert all(isinstance(user["id"], int) for user in data)

    assert data[0]["id"] < data[1]["id"]
