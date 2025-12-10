"""Module containing Message repository implementation."""

from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.MessagesOrm import MessagesOrm


class IMessageRepository(ABC):
    """An abstract base class representing a message repository."""

    @abstractmethod
    async def create_message(
        self,
        session: AsyncSession,
        sender_id: UUID,
        receiver_id: UUID,
        text: str,
    ) -> MessagesOrm:
        """Create a new message entry."""

    @abstractmethod
    async def get_user_messages(
        self,
        session: AsyncSession,
        owner_id: UUID,
    ) -> list[MessagesOrm]:
        """Retrieve messages involving the given user."""