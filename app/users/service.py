from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


async def list_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result = await session.scalars(statement)
    return list(result.all())
