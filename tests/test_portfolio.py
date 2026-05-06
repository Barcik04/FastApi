import unittest
from unittest import mock

from fastapi import HTTPException

from src.core.domain.Portfolio import Portfolio
from src.infrastructure.models import PortfolioOrm
from src.infrastructure.services.PortfolioService import PortfolioService

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone, timedelta, date

class PortfolioTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.flush = AsyncMock()



    async def test_show_user_portfolio_and_session_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.show_user_portfolio(uuid4(), None)

        self.assertEqual(context.exception.args[0], "session cannot be None")


    async def test_show_user_portfolio_and_owner_id_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService(self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.show_user_portfolio(None, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_show_user_requests_and_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)


        with self.assertRaises(ValueError) as context:
            await self.service.show_user_portfolio(uuid4(), self.session)

        self.assertEqual(context.exception.args[0], "user has no portfolio")


    async def test_show_user_request_happy_path(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={"bitcoin": 50000.0},
            p_and_l=100.0,
        )



        self.portfolio_repository = MagicMock()

        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "bitcoin": {
                "usd": 60000.0
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("src.infrastructure.services.PortfolioService.httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client

            result = await self.service.show_user_portfolio(owner_id, self.session)

        self.assertEqual(result, portfolio)




    async def test_show_user_portfolio_missing_bought_price(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=0.0,
        )

        self.portfolio_repository = MagicMock()
        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "bitcoin": {
                "usd": 60000.0
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("src.infrastructure.services.PortfolioService.httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client

            with self.assertRaises(ValueError) as context:
                await self.service.show_user_portfolio(owner_id, self.session)

        self.assertEqual(
            context.exception.args[0],
            "missing bought price for coin: bitcoin"
        )



    async def test_buy_crypto_and_session_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "bitcoin", 10.0, None)

        self.assertEqual(context.exception.args[0], "session cannot be None")


    async def test_buy_crypto_and_owner_id_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(None, "bitcoin", 10.0, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_buy_crypto_and_coin_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), None, 10.0, self.session)

        self.assertEqual(context.exception.args[0], "coin cannot be None")


    async def test_buy_crypto_and_coin_is_empty(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "", 10.0, self.session)

        self.assertEqual(context.exception.args[0], "coin cannot be empty")


    async def test_buy_crypto_and_quantity_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "bitcoin", None, self.session)

        self.assertEqual(context.exception.args[0], "quantity cannot be None")


    async def test_buy_crypto_and_quantity_is_negative(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "bitcoin", -1, self.session)

        self.assertEqual(context.exception.args[0], "quantity cannot be 0 or lower")



    async def test_buy_crypto_and_quantity_is_zero(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService( self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "bitcoin", 0, self.session)

        self.assertEqual(context.exception.args[0], "quantity cannot be 0 or lower")


    async def test_buy_crypto_and_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()

        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)


        with self.assertRaises(ValueError) as context:
            await self.service.buy_crypto(uuid4(), "bitcoin", 10.0, self.session)

        self.assertEqual(context.exception.args[0], "user has no portfolio")


    async def test_buy_crypto_not_enough_tether(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"tether": 1000.0},
            bought_price={},
            p_and_l=0.0,
        )

        self.portfolio_repository = MagicMock()
        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "bitcoin": {
                "usd": 60000.0
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("src.infrastructure.services.PortfolioService.httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client

            with self.assertRaises(ValueError) as context:
                await self.service.buy_crypto(
                    owner_id=owner_id,
                    coin="bitcoin",
                    quantity=1.0,
                    session=self.session,
                )

        self.assertEqual(
            context.exception.args[0],
            "Not enough theater in your account to buy: 1.0 of bitcoin."
        )




    async def test_buy_crypto_happy_path(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"tether": 100000.0},
            bought_price={},
            p_and_l=0.0,
        )

        self.portfolio_repository = MagicMock()
        self.service = PortfolioService(self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "bitcoin": {
                "usd": 60000.0
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("src.infrastructure.services.PortfolioService.httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.__aenter__.return_value = mock_client

            result = await self.service.buy_crypto(
                owner_id=owner_id,
                coin="bitcoin",
                quantity=1.0,
                session=self.session,
            )

        self.assertEqual(result,f"Transaction successful! Bought: 1.0, of bitcoin, with price: 60000.0")


