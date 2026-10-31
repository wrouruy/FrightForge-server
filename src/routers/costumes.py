import logging

from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Suit, SuitStatus
from src.database import get_db
from src.schemas import SuitOut

logger = logging.getLogger(__name__)

class RequestBody(BaseModel):
    adjective: str
    creature: str
    accessory: str
    author: EmailStr


async def costumes_get(session: AsyncSession = Depends(get_db)):
    try:
        statement = select(Suit).where(Suit.status == SuitStatus.APPROVED)
        result = await session.execute(statement)
        suits = result.scalars().all()
        return JSONResponse(
            status_code=200,
            content={
                'ok': True,
                'suits': [
                    SuitOut.model_validate(suit).model_dump(mode='json')
                    for suit in suits
                ],
            }
        )
    except Exception:
        logger.exception("Unexpected error while getting list of suits")

        return JSONResponse(
            status_code=500,
            content={'ok': False, 'message': 'Unknown error occured'},
        )


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

        return JSONResponse(
            status_code=409,
            content={'ok': False, 'message': f'The email address "{body.author}" is already taken'},
        )

    except Exception:
        await session.rollback()
        logger.exception("Unexpected error while creating suit")

        return JSONResponse(
            status_code=500,
            content={'ok': False, 'message': 'Unknown error occured'},
        )

    return JSONResponse(status_code=201, content={'ok': True})
