import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from src.infrastructure.repositories.TransactionRepository import TransactionRepository
from src.infrastructure.models.TransactionOrm import TransactionOrm


class TestTransactionRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.repository = TransactionRepository()
        self.session = AsyncMock()

    async def test_show_user_transactions(self):
        owner_id = uuid4()

        transaction_1 = MagicMock(spec=TransactionOrm)
        transaction_2 = MagicMock(spec=TransactionOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [transaction_1, transaction_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_transactions(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [transaction_1, transaction_2])
        self.session.execute.assert_awaited_once()

    async def test_show_user_transactions_between_date(self):
        owner_id = uuid4()
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)

        transaction_1 = MagicMock(spec=TransactionOrm)
        transaction_2 = MagicMock(spec=TransactionOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [transaction_1, transaction_2]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_transactions_between_date(
            self.session,
            start_date,
            end_date,
            owner_id,
        )

        self.assertEqual(result, [transaction_1, transaction_2])
        self.session.execute.assert_awaited_once()

    async def test_show_user_transactions_between_date_by_coin(self):
        owner_id = uuid4()
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        coin = "bitcoin"

        transaction = MagicMock(spec=TransactionOrm)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [transaction]

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_transactions_between_date_by_coin(
            self.session,
            start_date,
            end_date,
            owner_id,
            coin,
        )

        self.assertEqual(result, [transaction])
        self.session.execute.assert_awaited_once()

    async def test_show_user_transactions_empty_list(self):
        owner_id = uuid4()

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_transactions(
            self.session,
            owner_id,
        )

        self.assertEqual(result, [])
        self.session.execute.assert_awaited_once()

