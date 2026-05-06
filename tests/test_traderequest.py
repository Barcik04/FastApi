import unittest
from unittest import mock

from fastapi import HTTPException

from src.core.domain.Portfolio import Portfolio
from src.core.domain.TradeRequest import TradeRequest, TradeStatus, TradeRequestIn
from src.infrastructure.models import TradeRequestOrm
from src.infrastructure.services.TradeRequestService import TradeRequestService

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone, timedelta, date

class TradeRequestsTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.flush = AsyncMock()



    async def test_show_user_requests_and_session_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.show_user_requests(uuid4(), None)

        self.assertEqual(context.exception.args[0], "session cannot be None")


    async def test_show_user_requests_and_owner_id_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.show_user_requests(None, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")


    async def test_show_user_requests_and_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)


        with self.assertRaises(ValueError) as context:
            await self.service.show_user_requests(uuid4(), self.session)

        self.assertEqual(context.exception.args[0], "user has no portfolio")
        self.trade_request_repository.show_user_requests.assert_not_called()


    async def test_show_user_request_happy_path(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        requests = [
            TradeRequest(
                coin="bitcoin",
                quantity=0.5,
                coin_get="xrp",
                quantity_get=100.0,
                receiver_id=uuid4(),
                id=uuid4(),
                status=TradeStatus.PENDING,
                created_at=datetime.now(timezone.utc)
            )
        ]

        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)
        self.trade_request_repository.show_user_requests = AsyncMock(return_value=requests)

        result = await self.service.show_user_requests(owner_id, self.session)

        self.assertEqual(result, requests)


    async def test_show_user_requests_returns_empty_list_when_no_requests(self):
        owner_id = uuid4()

        portfolio = Portfolio(
            name="name",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()
        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=portfolio)
        self.trade_request_repository.show_user_requests = AsyncMock(return_value=[])

        result = await self.service.show_user_requests(owner_id, self.session)

        self.assertEqual(result, [])




    async def test_create_user_request_and_session_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        tradeRequest = TradeRequestIn(
            coin="bitcoin",
            quantity=0.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        owner_id = uuid4()

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, owner_id, None)

        self.assertEqual(context.exception.args[0], "session cannot be None")
        self.portfolio_repository.show_user_portfolio.assert_not_called()
        self.portfolio_repository.find_portfolio_by_id.assert_not_called()





    async def test_create_user_request_and_owner_id_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        tradeRequest = TradeRequestIn(
            coin="bitcoin",
            quantity=0.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, None, self.session)

        self.assertEqual(context.exception.args[0], "owner_id cannot be None")





    async def test_create_user_request_and_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        tradeRequest = TradeRequestIn(
            coin="bitcoin",
            quantity=0.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=None)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, uuid4(), self.session)

        self.assertEqual(context.exception.args[0], "user has no portfolio")



    async def test_create_user_request_and_receiver_portfolio_is_none(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()

        tradeRequest = TradeRequestIn(
            coin="bitcoin",
            quantity=0.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=None)
        self.trade_request_repository.create_request = AsyncMock(return_value=tradeRequest)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, owner_id, self.session)

        self.assertEqual(context.exception.args[0], f"Couldnt find portfolio with given id: {tradeRequest.receiver_id}")




    async def test_create_user_request_and_user_doesnt_have_coins(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()
        owner_id2 = uuid4()

        tradeRequest = TradeRequestIn(
            coin="xrp",
            quantity=0.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=uuid4(),
            owner_id=owner_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )


        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=owner_id2,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=receiver_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, uuid4(), self.session)

        self.assertEqual(context.exception.args[0], f"There is no coin with that name in your portfolio: {tradeRequest.coin}")





    async def test_create_user_request_and_user_has_not_enough_coins(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()
        owner_id2 = uuid4()

        tradeRequest = TradeRequestIn(
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=uuid4(),
            owner_id=owner_id,
            coins={"xrp": 1.0},
            bought_price={},
            p_and_l=100.0,
        )


        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=owner_id2,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=receiver_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, uuid4(), self.session)

        self.assertEqual(context.exception.args[0], f"There is not enough quantity: {tradeRequest.quantity} of coin in your portfolio: {tradeRequest.coin}")





    async def test_create_user_request_successfully(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()
        owner_id2 = uuid4()

        tradeRequest = TradeRequestIn(
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=uuid4(),
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=uuid4(),
            owner_id=owner_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )


        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=owner_id2,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=receiver_portfolio)
        self.trade_request_repository.create_request = AsyncMock()

        result = await self.service.create_user_request(tradeRequest, owner_id, self.session)

        self.assertEqual(result, "Successfully created a trade request!")




    async def test_create_user_request_and_sending_coins_to_your_own_portfolio(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()
        receiver_id = uuid4()

        tradeRequest = TradeRequestIn(
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=100.0,
            receiver_id=receiver_id,
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=receiver_id,
            owner_id=owner_id,
            coins={"xrp": 7.0},
            bought_price={},
            p_and_l=100.0,
        )


        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=owner_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.create_user_request(tradeRequest, uuid4(), self.session)

        self.assertEqual(context.exception.args[0],  "You cannot send coins to the same portfolio you are sending from")




    async def test_throws_value_error_when_update_user_request_owner_wants_to_accept_it(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        owner_id = uuid4()
        owner_id2 = uuid4()

        trade_request = TradeRequestOrm(
            id=uuid4(),
            sender_id=owner_id,
            receiver_id=owner_id2,
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=1.0,
            status=TradeStatus.PENDING,
            created_at=datetime.now()
        )

        owner_portfolio = Portfolio(
            name="owner portfolio",
            id=uuid4(),
            owner_id=owner_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )


        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=owner_id2,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.trade_request_repository.find_request = AsyncMock(return_value=trade_request)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=owner_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=receiver_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.update_user_request(owner_id, True, owner_id2, self.session)

        self.assertEqual(context.exception.args[0],  "This method was sent by you so you can only reject it")





    async def test_throws_value_error_when_update_user_request_and_trade_status_is_rejected(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        sender_user_id = uuid4()
        receiver_user_id = uuid4()

        sender_portfolio = Portfolio(
            name="sender portfolio",
            id=uuid4(),
            owner_id=sender_user_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )

        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=receiver_user_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        trade_request = TradeRequestOrm(
            id=uuid4(),
            sender_id=sender_portfolio.id,
            receiver_id=receiver_portfolio.id,
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=1.0,
            status=TradeStatus.REJECTED,
            created_at=datetime.now()
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.trade_request_repository.find_request = AsyncMock(return_value=trade_request)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=receiver_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=sender_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.update_user_request(receiver_user_id,True, trade_request.id, self.session)

        self.assertEqual(context.exception.args[0], "This trade has already been rejected or completed")





    async def test_throws_value_error_when_update_user_request_and_trade_status_is_completed(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        sender_user_id = uuid4()
        receiver_user_id = uuid4()

        sender_portfolio = Portfolio(
            name="sender portfolio",
            id=uuid4(),
            owner_id=sender_user_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )

        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=receiver_user_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        trade_request = TradeRequestOrm(
            id=uuid4(),
            sender_id=sender_portfolio.id,
            receiver_id=receiver_portfolio.id,
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=1.0,
            status=TradeStatus.COMPLETED,
            created_at=datetime.now()
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.trade_request_repository.find_request = AsyncMock(return_value=trade_request)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=receiver_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=sender_portfolio)

        with self.assertRaises(ValueError) as context:
            await self.service.update_user_request(receiver_user_id,True, trade_request.id, self.session)

        self.assertEqual(context.exception.args[0], "This trade has already been rejected or completed")







    async def test_update_user_request_and_accept_successfully(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        sender_user_id = uuid4()
        receiver_user_id = uuid4()

        sender_portfolio = Portfolio(
            name="sender portfolio",
            id=uuid4(),
            owner_id=sender_user_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )

        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=receiver_user_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        trade_request = TradeRequestOrm(
            id=uuid4(),
            sender_id=sender_portfolio.id,
            receiver_id=receiver_portfolio.id,
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=1.0,
            status=TradeStatus.PENDING,
            created_at=datetime.now()
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.trade_request_repository.find_request = AsyncMock(return_value=trade_request)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=receiver_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=sender_portfolio)

        self.service._proceed_trade = AsyncMock()

        result = await self.service.update_user_request(receiver_user_id,True, trade_request.id, self.session)

        self.assertEqual(result, "trade accepted!")
        self.assertEqual(trade_request.status, TradeStatus.COMPLETED)

        self.service._proceed_trade.assert_awaited_once_with(
            session=self.session,
            request=trade_request,
            sender_portfolio=sender_portfolio,
            receiver_portfolio=receiver_portfolio,
        )





    async def test_update_user_request_and_reject_successfully(self):
        self.portfolio_repository = MagicMock()
        self.trade_request_repository = MagicMock()

        sender_user_id = uuid4()
        receiver_user_id = uuid4()

        sender_portfolio = Portfolio(
            name="sender portfolio",
            id=uuid4(),
            owner_id=sender_user_id,
            coins={"xrp": 9.0},
            bought_price={},
            p_and_l=100.0,
        )

        receiver_portfolio = Portfolio(
            name="receiver portfolio",
            id=uuid4(),
            owner_id=receiver_user_id,
            coins={"bitcoin": 1.0},
            bought_price={},
            p_and_l=100.0,
        )

        trade_request = TradeRequestOrm(
            id=uuid4(),
            sender_id=sender_portfolio.id,
            receiver_id=receiver_portfolio.id,
            coin="xrp",
            quantity=6.5,
            coin_get="xrp",
            quantity_get=1.0,
            status=TradeStatus.PENDING,
            created_at=datetime.now()
        )

        self.service = TradeRequestService(self.trade_request_repository, self.portfolio_repository)

        self.trade_request_repository.find_request = AsyncMock(return_value=trade_request)
        self.portfolio_repository.show_user_portfolio = AsyncMock(return_value=receiver_portfolio)
        self.portfolio_repository.find_portfolio_by_id = AsyncMock(return_value=sender_portfolio)

        self.service._proceed_trade = AsyncMock()

        result = await self.service.update_user_request(receiver_user_id, False, trade_request.id, self.session)

        self.assertEqual(result, "trade rejected!")
        self.assertEqual(trade_request.status, TradeStatus.REJECTED)

        self.service._proceed_trade.assert_not_awaited()

























