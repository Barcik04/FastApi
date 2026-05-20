import unittest
from unittest import mock

from fastapi import HTTPException

from src.core.domain.Message import Message
from src.infrastructure.models import MessagesOrm
from src.infrastructure.services.MessageService import MessageService
from src.core.domain.Message import MessageIn

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone, timedelta, date


class MessagesTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.flush = AsyncMock()

        self.message_repository = MagicMock()
        self.service = MessageService(self.message_repository)

    async def test_send_message_happy_path(self):
        sender_id = uuid4()
        receiver_id = uuid4()
        message_id = uuid4()

        data = MessageIn(
            text="Hello bro",
            receiver_id=receiver_id,
        )

        message = Message(
            id=message_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            text="Hello bro",
            created_at=datetime.now(timezone.utc),
        )

        self.message_repository.create_message = AsyncMock(return_value=message)

        result = await self.service.send_message(
            data=data,
            sender_id=sender_id,
            session=self.session,
        )

        self.assertEqual(result, message)


    async def test_show_user_messages_happy_path(self):
        owner_id = uuid4()

        message1 = Message(
            id=uuid4(),
            sender_id=owner_id,
            receiver_id=uuid4(),
            text="First message",
            created_at=datetime.now(timezone.utc),
        )

        message2 = Message(
            id=uuid4(),
            sender_id=uuid4(),
            receiver_id=owner_id,
            text="Second message",
            created_at=datetime.now(timezone.utc),
        )

        messages = [message1, message2]

        self.message_repository.get_user_messages = AsyncMock(return_value=messages)

        result = await self.service.show_user_messages(
            owner_id=owner_id,
            session=self.session,
        )

        self.assertEqual(result, messages)
