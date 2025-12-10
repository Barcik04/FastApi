"""Module containing message service implementation."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.Message import Message, MessageIn
from src.infrastructure.models import MessagesOrm
from src.infrastructure.repositories.MessageRepository import MessageRepository
from src.infrastructure.services.IMessageService import IMessageService


class MessageService(IMessageService):
    """A class implementing the message service."""

    def __init__(self, repo: MessageRepository | None = None):
        self.repo = repo or MessageRepository()

    async def send_message(self, body: MessageIn, sender_id: UUID, session: AsyncSession) -> Message:
        """The method sending a message to some user"""

        async with session.begin():
            message = await self.repo.create_message(session, sender_id=sender_id, receiver_id=body.receiver_id, text=body.text,)

            return Message.model_validate(message)

    async def show_user_messages(self, owner_id: UUID, session: AsyncSession) -> list[MessagesOrm]:
        """The method fetching all messages where the user is sender or receiver."""

        async with session.begin():
            messages = await self.repo.get_user_messages(session, owner_id)
            return messages