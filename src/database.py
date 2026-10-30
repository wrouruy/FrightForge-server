import os
from pathlib import Path

from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import ssl

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env.local")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to .env.local in the project root."
    )

# ssl_context = ssl.create_default_context() # ssl context for neon db

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session