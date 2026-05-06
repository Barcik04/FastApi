"""Module containing transaction-related domain models."""

from datetime import datetime

from pydantic import ConfigDict, BaseModel
from uuid import UUID


class Transaction(BaseModel):
    """Model representing transaction attributes stored in the database."""

    id: UUID
    owner_id: UUID
    coin: str
    date: datetime
    quantity: float
    bought_price: float
    model_config = ConfigDict(from_attributes=True, extra="ignore")
