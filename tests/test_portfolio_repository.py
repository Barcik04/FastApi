import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.infrastructure.repositories.PortfolioRepository import PortfolioRepository
from src.infrastructure.models.PortfolioOrm import PortfolioOrm


class TestPortfolioRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.repository = PortfolioRepository()
        self.session = AsyncMock()

    async def test_show_user_portfolio_found(self):
        owner_id = uuid4()

        portfolio = MagicMock(spec=PortfolioOrm)

        mock_result = MagicMock()
        mock_result.scalar.return_value = portfolio

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_portfolio(
            self.session,
            owner_id,
        )

        self.assertEqual(result, portfolio)

    async def test_show_user_portfolio_not_found(self):
        owner_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar.return_value = None

        self.session.execute.return_value = mock_result

        result = await self.repository.show_user_portfolio(
            self.session,
            owner_id,
        )

        self.assertIsNone(result)

    async def test_find_portfolio_by_id_found(self):
        portfolio_id = uuid4()

        portfolio = MagicMock(spec=PortfolioOrm)

        mock_result = MagicMock()
        mock_result.scalar.return_value = portfolio

        self.session.execute.return_value = mock_result

        result = await self.repository.find_portfolio_by_id(
            self.session,
            portfolio_id,
        )

        self.assertEqual(result, portfolio)

    async def test_find_portfolio_by_id_not_found(self):
        portfolio_id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar.return_value = None

        self.session.execute.return_value = mock_result

        result = await self.repository.find_portfolio_by_id(
            self.session,
            portfolio_id,
        )

        self.assertIsNone(result)

