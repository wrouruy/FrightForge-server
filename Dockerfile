FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml /code/pyproject.toml
COPY ./uv.lock /code/uv.lock
COPY ./.env.local /code/.env.local

RUN uv sync --frozen --no-editable && uv cache clean

COPY ./src /code/src

CMD ["sh", "-c", "uv run uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]