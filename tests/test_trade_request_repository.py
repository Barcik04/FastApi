import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.infrastructure.repositories.TradeRequestRepository import TradeRequestRepository
from src.infrastructure.models.TradeRequestOrm import TradeRequestOrm


class TestTradeRequestRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.repository = TradeRequestRepository()
        self.session = AsyncMock()

    async def test_show_user_requests(self):
        owner_id = uuid4()

        request_1 = MagicMock(spec=TradeRequestOrm)
        request_2 = MagicMock(spec=TradeRequestOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [request_1, request_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_requests(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [request_1, request_2])
        self.session.execute.assert_awaited_once()

    async def test_show_user_senders(self):
        owner_id = uuid4()

        request_1 = MagicMock(spec=TradeRequestOrm)
        request_2 = MagicMock(spec=TradeRequestOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [request_1, request_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_senders(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [request_1, request_2])

    async def test_show_user_receivers(self):
        owner_id = uuid4()

        request_1 = MagicMock(spec=TradeRequestOrm)
        request_2 = MagicMock(spec=TradeRequestOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [request_1, request_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_receivers(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [request_1, request_2])

    async def test_create_request(self):
        sender_id = uuid4()
        receiver_id = uuid4()

        result = await self.repository.create_request(
            session=self.session,
            coin="bitcoin",
            quantity=1.0,
            coin_get="ethereum",
            quantity_get=10.0,
            sender_id=sender_id,
            receiver_id=receiver_id,
        )

        self.assertIsInstance(result, TradeRequestOrm)
        self.assertEqual(result.sender_id, sender_id)
        self.assertEqual(result.receiver_id, receiver_id)
        self.assertEqual(result.coin, "bitcoin")


    async def test_find_request_found(self):
        request_id = uuid4()

        trade_request = MagicMock(spec=TradeRequestOrm)

        mock_result = MagicMock()
        mock_result.scalar.return_value = trade_request

        self.session.execute.return_value = mock_result

        result = await self.repository.find_request(
            self.session,
            request_id,
        )

        self.assertEqual(result, trade_request)
        self.session.execute.assert_awaited_once()

    async def test_find_request_not_found(self):
        request_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar.return_value = None

        self.session.execute.return_value = mock_result

        result = await self.repository.find_request(
            self.session,
            request_id,
        )

        self.assertIsNone(result)
        self.session.execute.assert_awaited_once()

    async def test_show_user_requests_empty_list(self):
        owner_id = uuid4()

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_requests(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [])
        self.session.execute.assert_awaited_once()
