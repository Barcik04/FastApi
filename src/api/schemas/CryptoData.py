from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CryptoData(BaseModel):
    id: UUID
    owner_id: UUID
    amount: float
    amount_p_and_l: float
    date: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
