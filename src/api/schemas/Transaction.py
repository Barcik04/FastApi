from datetime import datetime

from pydantic import ConfigDict
from uuid import UUID


class Transaction:
    id: UUID
    owner_id: UUID
    coin: str
    amount: float
    date: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")