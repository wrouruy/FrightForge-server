import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import ssl

load_dotenv(dotenv_path=".env.local")

DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context() # ssl context for neon db

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context}
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