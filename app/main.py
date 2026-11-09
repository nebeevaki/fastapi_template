from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.session import engine


# выполнение кода при запуске и завершении приложения
@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        # закрываем все соединения из пула и заменяем сам пул на новый и пустой
        await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)  # создаем ASGI-приложение

# подключаем центральный маршрутизатор со всеми эндпоинтами
app.include_router(api_router)
