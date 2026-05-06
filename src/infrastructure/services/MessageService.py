"""Module containing message service implementation."""

from typing import Iterable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.Message import Message, MessageIn
from src.core.irepositories.imessage import IMessageRepository
from src.infrastructure.models import MessagesOrm
from src.infrastructure.services.IMessageService import IMessageService


class MessageService(IMessageService):
    """A class implementing the message service."""

    _repository: IMessageRepository

    def __init__(self, repository: IMessageRepository) -> None:
        """The initializer of the `message service`.

        Args:
            repository (IMessageRepository): The reference to the repository.
        """
        self._repository = repository

    async def send_message(
        self,
        data: MessageIn,
        sender_id: UUID,
        session: AsyncSession,
    ) -> MessagesOrm:
        """The method sending a message to some user.

        Args:
            data (MessageIn): The attributes of the message.
            sender_id (UUID): The sender id.
            session (AsyncSession): The database session.

        Returns:
            Message | None: The newly created message.
        """

        return await self._repository.create_message(
            session=session,
            sender_id=sender_id,
            receiver_id=data.receiver_id,
            text=data.text,
        )

    async def show_user_messages(
        self,
        owner_id: UUID,
        session: AsyncSession,
    ) -> list[MessagesOrm]:
        """The method fetching all messages where the user is sender or receiver.

        Args:
            owner_id (UUID): The user id.
            session (AsyncSession): The database session.

        Returns:
            Iterable[Message]: The collection of user messages.
        """

        return await self._repository.get_user_messages(
            session=session,
            owner_id=owner_id,
        )
