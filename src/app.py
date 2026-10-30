from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import engine, Base, get_db
from src.models import Suit

from src.routers import (
    generate,
    costumes_get,
    costumes_post
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI()

@app.get('/health')
async def health(): # ping analogue
    return { 'ok': True }


@app.get('/')
async def root():
    return { "hello": "world!" }


router = APIRouter()
router.add_api_route('/generate', endpoint=generate, methods=['GET'])
router.add_api_route('/costumes', endpoint=costumes_get, methods=['GET'])
router.add_api_route('/costumes', endpoint=costumes_post, methods=['POST'])

app.include_router(router)