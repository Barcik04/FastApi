import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.infrastructure.repositories.MessageRepository import MessageRepository
from src.infrastructure.models.MessagesOrm import MessagesOrm


class TestMessageRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.repository = MessageRepository()
        self.session = AsyncMock()

    async def test_create_message(self):
        sender_id = uuid4()
        receiver_id = uuid4()

        result = await self.repository.create_message(
            session=self.session,
            sender_id=sender_id,
            receiver_id=receiver_id,
            text="hello",
        )

        self.assertEqual(result.sender_id, sender_id)
        self.assertEqual(result.receiver_id, receiver_id)
        self.assertEqual(result.text, "hello")


    async def test_get_user_messages(self):
        owner_id = uuid4()

        message_1 = MagicMock(spec=MessagesOrm)
        message_2 = MagicMock(spec=MessagesOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [message_1, message_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.get_user_messages(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [message_1, message_2])

    async def test_get_user_messages_empty_list(self):
        owner_id = uuid4()

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.get_user_messages(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [])

