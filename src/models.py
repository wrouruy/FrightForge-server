from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SQLEnum, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class SuitStatus(str, Enum):
    PENDING = "pending",
    APPROVED = "approved",
    REJECTED = "rejected"

class Suit(Base):
    __tablename__ = "suits"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[SuitStatus] = mapped_column(
        default=SuitStatus.PENDING
    )

    # description for parts of suit
    adjective: Mapped[str] = mapped_column(String(50))
    creature: Mapped[str] = mapped_column(String(50))
    accessory: Mapped[str] = mapped_column(String(50))

    author: Mapped[str] = mapped_column(String(100), unique=True) # email field
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )