import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Suit, SuitStatus
from src.schemas import SuitOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


class PendingCostumesResponse(BaseModel):
    ok: bool
    suits: list[SuitOut]


@router.get("/costumes", response_model=PendingCostumesResponse)
async def pending_costumes(
    session: AsyncSession = Depends(get_db),
):
    try:
        statement = (
            select(Suit)
            .where(Suit.status == SuitStatus.PENDING)
            .order_by(Suit.created_at.asc())
        )
        result = await session.execute(statement)
        suits = result.scalars().all()

        return PendingCostumesResponse(
            ok=True,
            suits=[SuitOut.model_validate(suit) for suit in suits],
        )
    except Exception:
        logger.exception("Unexpected error while getting list of pending suits")

        return JSONResponse(
            status_code=500,
            content={"ok": False, "message": "Unknown error occured"},
        )
