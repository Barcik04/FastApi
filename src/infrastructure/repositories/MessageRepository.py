"""Module containing Message repository implementation."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.irepositories.imessage import IMessageRepository
from src.infrastructure.models.MessagesOrm import MessagesOrm


class MessageRepository(IMessageRepository):
    """A class responsible for performing message-related DB operations."""

    async def create_message(self, session: AsyncSession, sender_id: UUID, receiver_id: UUID,text: str,) -> MessagesOrm:
        """Create and persist a message instance."""
        message = MessagesOrm(sender_id=sender_id,receiver_id=receiver_id,text=text)
        session.add(message)
        return message

    async def get_user_messages(self,session: AsyncSession,owner_id: UUID,) -> list[MessagesOrm]:
        """The method getting messages where the user is sender or receiver."""
        res = await session.execute(
            select(MessagesOrm).where((MessagesOrm.sender_id == owner_id) | (MessagesOrm.receiver_id == owner_id))
            .order_by(MessagesOrm.created_at.desc()))

        return res.scalars().all()