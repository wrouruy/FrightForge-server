import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Suit, SuitStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])

class SetStatusRequest(BaseModel):
    status: Literal[SuitStatus.APPROVED, SuitStatus.REJECTED]


@router.patch("/costumes/{suit_id}")
async def set_costume_status(
    suit_id: int,
    body: SetStatusRequest,
    session: AsyncSession = Depends(get_db),
):
    try:
        suit = await session.get(Suit, suit_id)
        if suit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suit not found",
            )

        suit.status = body.status
        await session.commit()
        await session.refresh(suit)
    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        logger.exception("Unexpected error while updating suit status")

        return JSONResponse(
            status_code=500,
            content={"ok": False, "message": "Unknown error occured"},
        )

    return {
        "ok": True,
        "suit": {"id": suit.id, "status": suit.status},
    }
