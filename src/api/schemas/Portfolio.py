from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PortfolioIn(BaseModel):
    name: str


class Portfolio(PortfolioIn):
    id: UUID
    owner_id: UUID
    coins: dict[str, float]
    bought_price: dict[str, float]
    p_and_l: float
    model_config = ConfigDict(from_attributes=True, extra="ignore")