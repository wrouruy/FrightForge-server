from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.models import SuitStatus

class SuitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: SuitStatus
    adjective: str
    creature: str
    accessory: str
    author: str
    created_at: datetime
