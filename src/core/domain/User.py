"""Module containing user-related domain models."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserIn(BaseModel):
    """Model representing user DTO attributes."""

    email: str
    password: str


class User(UserIn):
    """Model representing user attributes stored in the database."""

    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")
