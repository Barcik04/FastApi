"""Module containing message-related domain models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MessageIn(BaseModel):
    """Model representing message DTO attributes."""

    text: str
    receiver_id: UUID


class Message(MessageIn):
    """Model representing message DTO attributes."""

    id: UUID
    sender_id: UUID
    receiver_id: UUID
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
