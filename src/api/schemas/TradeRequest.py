from datetime import datetime

from enum import Enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TradeStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

class TradeRequestIn(BaseModel):
    coin: str
    quantity: float
    portfolio_id: UUID

class TradeRequest(TradeRequestIn):
    id: UUID
    status: TradeStatus = TradeStatus.PENDING
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")
