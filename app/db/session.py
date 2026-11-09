from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# центральный объект SQLAlchemy для взаимодействия с асинхронным драйвером БД
engine = create_async_engine(
    str(settings.database_url),  # url database
    pool_pre_ping=True,  # проверка соединения с БД перед выдачей его из пула
)

# фабрика создания новых сессий
session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# зависимость для получения сессии(FastAPI)
async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


# алиас для упрощения аннотации типа
SessionDep = Annotated[AsyncSession, Depends(get_session)]
