import logging

from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Suit
from src.database import get_db

logger = logging.getLogger(__name__)

class RequestBody(BaseModel):
    adjective: str
    creature: str
    accessory: str
    author: EmailStr


async def costumes_get(session: AsyncSession = Depends(get_db)):
    pass


async def costumes_post(
    body: RequestBody,
    session: AsyncSession = Depends(get_db),
):
    try:
        new_suit = Suit(
            adjective=body.adjective,
            creature=body.creature,
            accessory=body.accessory,
            author=body.author,
        )

        session.add(new_suit)
        await session.commit()

    except IntegrityError:
        await session.rollback()
        logger.exception("Failed to insert suit")

        return JSONResponse(
            status_code=500,
            content={'ok': False, 'message': 'DataBase Internal error'},
        )

    except Exception:
        await session.rollback()
        logger.exception("Unexpected error while creating suit")

        return JSONResponse(
            status_code=500,
            content={'ok': False, 'message': 'Unknown error occured'},
        )

    return JSONResponse(status_code=201, content={'ok': True})
