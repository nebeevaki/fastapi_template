# Базовый образ Python
FROM python:3.12-slim-bookworm

# uv из официального образа Astral
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /bin/

# Настройки uv и PATH
ENV UV_PYTHON_DOWNLOADS=0 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Рабочий каталог внутри контейнера
WORKDIR /app

# Сначала копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем только runtime-зависимости
RUN uv sync --locked --no-dev --no-install-project

# Копируем исходный код
COPY app ./app

# Создаем непривилегированного пользователя
RUN groupadd --system appgroup \
    && useradd --system --uid 10001 --gid appgroup appuser \
    && chown -R appuser:appgroup /app

USER appuser

# Документируем порт приложения
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

