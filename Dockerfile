FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-editable \
    && uv cache clean

COPY . .

CMD ["sh", "-c", "uv run uvicorn app.app:app --host 0.0.0.0 --port ${PORT:-8000}"]