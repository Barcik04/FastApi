"""Module containing message service abstractions."""

from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.Message import Message, MessageIn


class IMessageService(ABC):
    """An abstract class representing a message service."""

    @abstractmethod
    async def send_message(
        self, body: MessageIn, sender_id: UUID, session: AsyncSession
    ) -> Message:
        """Send a message"""

    @abstractmethod
    async def show_user_messages(
        self, owner_id: UUID, session: AsyncSession
    ) -> list[Message]:
        """Retrieve messages for the given user."""
