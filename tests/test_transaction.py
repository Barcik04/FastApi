import unittest
from unittest import mock

from fastapi import HTTPException

from src.core.domain.Portfolio import Portfolio
from src.core.domain.Transaction import Transaction
from src.infrastructure.services.TransactionService import TransactionService

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone, timedelta, date


class TransactionTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.flush = AsyncMock()




    async def test_list_for_user_successfully(self):
        owner_id = uuid4()
        transactions = [
            Transaction(id=uuid4(), owner_id=owner_id, coin="BTC", date=date(2019, 12, 12), quantity=100.00, bought_price=89000.00),
            Transaction(id=uuid4(), owner_id=owner_id, coin="BTC", date=date(2020, 12, 12), quantity=100.00, bought_price=89000.00)
        ]

        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()
        self.transaction_repository.show_user_transactions = AsyncMock(return_value=transactions)

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        result = await self.service.list_for_user(owner_id, self.session)

        self.assertEqual(result, transactions)
        self.assertEqual(result[0], transactions[0])




    async def test_list_for_user_returns_empty_list_when_no_transactions(self):
        owner_id = uuid4()

        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()
        self.transaction_repository.show_user_transactions = AsyncMock(return_value=[])

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        result = await self.service.list_for_user(owner_id, self.session)

        self.assertEqual(result, [])
        self.transaction_repository.show_user_transactions.assert_awaited_once_with(
            self.session, owner_id
        )


    async def test_raises_exception_when_owner_id_if_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.list_for_user(None, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_raises_exception_when_days_below_0_graph_portfolio_value(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_portfolio_val(uuid4(), -1, self.session)

        self.assertEqual(context.exception.args[0], "Number of days cant be 0 or less")




    async def test_raises_exception_when_owner_id_is_none_graph_portfolio_val(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_portfolio_val(None, 1, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")




    async def test_raises_exception_when_owner_does_not_have_portfolio(self):
        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_portfolio_val(uuid4(), 1, self.session)

        self.assertEqual(context.exception.args[0], "portfolio of given user is None")



    async def test_raises_exception_when_only_tether_graph_portfolio_value(self):
        owner_id = uuid4()
        coins = {"tether": 100.00}
        bought_price = {"tether": 89000.00}
        portfolio = Portfolio(name="name", id=uuid4(), owner_id=owner_id, coins=coins, bought_price=bought_price, p_and_l=100.00)

        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_portfolio_val(owner_id, 1, self.session)

        self.assertEqual(context.exception.args[0], "No graphable coins in portfolio")




    async def test_raises_exception_when_portfolio_empty(self):
        owner_id = uuid4()
        portfolio = Portfolio(name="name", id=uuid4(), owner_id=owner_id, coins={}, bought_price={},
                              p_and_l=100.00)

        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_portfolio_val(owner_id, 1, self.session)

        self.assertEqual(context.exception.args[0], "No graphable coins in portfolio")





    @patch("src.infrastructure.services.TransactionService.httpx.AsyncClient")
    async def test_graph_portfolio_val_happy_path_no_errors(self, mock_async_client):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0
        )


        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)
        self.transaction_repository.show_user_transactions_between_date_by_coin = AsyncMock(return_value=[])

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "prices": [
                [1710000000000, 50000.0],
                [1710086400000, 51000.0]
            ]
        }

        client = mock_async_client.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        mock_async_client.return_value.__aexit__.return_value = None

        result = await self.service.graph_portfolio_val(owner_id, 2, self.session)

        self.assertIsNotNone(result)
        self.assertEqual(result.media_type, "image/png")


        client.get.assert_awaited_once_with(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": "2"}
        )

        mock_response.raise_for_status.assert_called_once()



    async def test_raises_value_error_graph_multiple_coins_and_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_multiple_coins(uuid4(), 1, self.session)

        self.assertEqual(context.exception.args[0], "portfolio of given user is None")



    async def test_raises_value_error_when_graph_multiple_coins_and_owner_id_is_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_multiple_coins(None, 1, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_raises_value_error_when_graph_multiple_coins_and_session_is_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_multiple_coins(uuid4(), 1, None)

        self.assertEqual(context.exception.args[0], "session cannot be None")




    async def test_raises_value_error_when_graph_multiple_coins_and_days_negative(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_multiple_coins(uuid4(), -1, self.session)

        self.assertEqual(context.exception.args[0], "Number of days cant be 0 or less")




    async def test_raises_value_error_when_graph_multiple_coins_and_portfolio_is_empty(self):
        owner_id = uuid4()
        portfolio = Portfolio(name="name", id=uuid4(), owner_id=owner_id, coins={}, bought_price={},
                              p_and_l=0.00)

        self.transaction_repository = MagicMock()
        self.portfolio_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_multiple_coins(owner_id, 1, self.session)


        self.assertEqual(context.exception.args[0], "No graphable coins in portfolio")




    @patch("src.infrastructure.services.TransactionService.httpx.AsyncClient")
    async def test_graph_multiple_coins_happy_path_no_errors(self, mock_async_client):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0
        )


        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)
        self.transaction_repository.show_user_transactions_between_date_by_coin = AsyncMock(return_value=[])

        self.service = TransactionService(self.transaction_repository, self.portfolio_repository)

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "prices": [
                [1710000000000, 50000.0],
                [1710086400000, 51000.0]
            ]
        }

        client = mock_async_client.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        mock_async_client.return_value.__aexit__.return_value = None

        result = await self.service.graph_multiple_coins(owner_id, 2, self.session)

        self.assertIsNotNone(result)
        self.assertEqual(result.media_type, "image/png")


        client.get.assert_awaited_once_with(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": "2"}
        )

        mock_response.raise_for_status.assert_called_once()




    async def test_raises_value_error_when_graph_p_n_l_percent_and_owner_id_is_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_p_n_l_percent(None, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_raises_value_error_when_graph_p_n_l_percent_and_session_is_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_p_n_l_percent(uuid4(),None)

        self.assertEqual(context.exception.args[0], "session cannot be None")


    async def test_raises_value_error_when_graph_p_n_l_percent_and_no_transactions(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)



    @patch("src.infrastructure.services.TransactionService.httpx.AsyncClient")
    async def test_graph_p_n_l_percent_happy_path_no_errors(self, mock_async_client):
        owner_id = uuid4()

        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(
            self.transaction_repository,
            self.portfolio_repository
        )

        transaction_date = datetime.now(timezone.utc) - timedelta(days=2)

        transaction_1 = MagicMock()
        transaction_1.bought_price = 50000.0
        transaction_1.date = transaction_date
        transaction_1.coin = "bitcoin"

        transaction_2 = MagicMock()
        transaction_2.bought_price = 50000.0
        transaction_2.date = transaction_date
        transaction_2.coin = "bitcoin"

        self.transaction_repository.show_user_transactions = AsyncMock(
            return_value=[transaction_1, transaction_2]
        )

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "prices": [
                [1710000000000, 50000.0],
                [1710086400000, 51000.0]
            ]
        }

        client = mock_async_client.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        mock_async_client.return_value.__aexit__.return_value = None

        result = await self.service.graph_p_n_l_percent(owner_id, self.session)

        self.assertIsNotNone(result)
        self.assertEqual(result.media_type, "image/png")

        client.get.assert_any_await(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": "2"}
        )

        self.assertEqual(client.get.await_count, 3)


    async def test_raises_value_error_when_graph_p_n_l_and_session_is_none(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_p_n_l(uuid4(),None)

        self.assertEqual(context.exception.args[0], "session cannot be None")


    async def test_raises_value_error_when_graph_p_n_l_and_owner_id_is_none(self):
        owner_id = None

        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()
        self.service = TransactionService(self.transaction_repository, self.user_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.graph_p_n_l(owner_id,self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")



    async def test_raises_value_error_when_graph_p_n_l_and_no_coins(self):
        self.user_repository = MagicMock()
        self.transaction_repository = MagicMock()

        owner_id = uuid4()

        self.service = TransactionService(self.transaction_repository, self.user_repository)

        self.transaction_repository.show_user_transactions = AsyncMock(return_value=[])

        with self.assertRaises(HTTPException) as context:
            await self.service.graph_p_n_l(owner_id,self.session)

        self.assertEqual(
            context.exception.detail,
            "No purchase transactions found for the user",
        )




    @patch("src.infrastructure.services.TransactionService.httpx.AsyncClient")
    async def test_graph_p_n_l_happy_path_no_errors(self, mock_async_client):
        owner_id = uuid4()

        self.portfolio_repository = MagicMock()
        self.transaction_repository = MagicMock()

        self.service = TransactionService(
            self.transaction_repository,
            self.portfolio_repository
        )

        transaction_date = datetime.now(timezone.utc) - timedelta(days=2)

        transaction_1 = MagicMock()
        transaction_1.bought_price = 50000.0
        transaction_1.date = transaction_date
        transaction_1.coin = "bitcoin"

        transaction_2 = MagicMock()
        transaction_2.bought_price = 50000.0
        transaction_2.date = transaction_date
        transaction_2.coin = "bitcoin"

        self.transaction_repository.show_user_transactions = AsyncMock(
            return_value=[transaction_1, transaction_2]
        )

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "prices": [
                [1710000000000, 50000.0],
                [1710086400000, 51000.0]
            ]
        }

        client = mock_async_client.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        mock_async_client.return_value.__aexit__.return_value = None

        result = await self.service.graph_p_n_l(owner_id, self.session)

        self.assertIsNotNone(result)
        self.assertEqual(result.media_type, "image/png")

        client.get.assert_any_await(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": mock.ANY}
        )

        self.assertEqual(client.get.await_count, 3)