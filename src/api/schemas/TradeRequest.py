"""Module containing trade request-related domain models."""

from datetime import datetime

from enum import Enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TradeStatus(str, Enum):
    """Enum representing trade request status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

class TradeRequestIn(BaseModel):
    """Model representing trade request DTO attributes."""
    coin: str
    quantity: float
    coin_get: str
    quantity_get: float
    receiver_id: UUID

class TradeRequest(TradeRequestIn):
    """Model representing trade request attributes stored in the database."""
    id: UUID
    status: TradeStatus = TradeStatus.PENDING
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TradeRequestUpdateDto(BaseModel):
    """DTO model used for updating trade request status."""
    accept: bool
    request_id: UUID