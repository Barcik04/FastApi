"""Module containing portfolio-related domain models."""


from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PortfolioIn(BaseModel):
    """Model representing portfolio DTO attributes."""
    name: str


class Portfolio(PortfolioIn):
    """Model representing portfolio attributes stored in the database."""
    id: UUID
    owner_id: UUID
    coins: dict[str, float]
    bought_price: dict[str, float]
    p_and_l: float
    model_config = ConfigDict(from_attributes=True, extra="ignore")

