"""Module containing trade request service implementation."""
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.TradeRequestOrm import TradeRequestOrm
from src.infrastructure.repositories.PortfolioRepository import PortfolioRepository
from src.infrastructure.repositories.TradeRequestRepository import TradeRequestRepository
from uuid import UUID

from src.infrastructure.services.ITradeRequestService import ITradeRequestService

from src.core.domain.TradeRequest import TradeRequestIn, TradeStatus



class TradeRequestService(ITradeRequestService):
    """A class implementing the trade request service."""
    def __init__(self,
                 trade_request_repo: TradeRequestRepository | None = None,
                 portfolio_repo: PortfolioRepository | None = None,
                 ):
        self.trade_request_repo = trade_request_repo or TradeRequestRepository()
        self.portfolio_repo = portfolio_repo or PortfolioRepository()




    async def show_user_requests(self, owner_id: UUID, session: AsyncSession) -> list[TradeRequestOrm]:
        """The method getting trade requests assigned to particular user.

                   Args:
                       owner_id (int): The id of the user.
                       session (AsyncSession): database session.

                   Returns:
                       list[TradeRequestOrm]: list of trade requests assigned to a particular user.
               """


        async with session.begin():
            portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)
            requests = await self.trade_request_repo.show_user_requests(session, portfolio.id)

            return requests





    async def create_user_request(self, body: TradeRequestIn, owner_id: UUID, session: AsyncSession) -> str:
        """The method creates a trade request aimed to a particular user specified in body with coin and quantity.

            Args:
                owner_id (int): The id of the user.
                body (TradeRequestIn): The body DTO of the trade request contains: (coin: str, quantity: float, coin_get: str, quantity_get: float, receiver_id: UUID)
                session (AsyncSession): database session.

            Returns:
                str: info of transaction status.
        """

        async with session.begin():

            portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)
            if portfolio is None:
                raise HTTPException(status_code=404, detail="Sender portfolio not found")

            portfolio_receiver = await self.portfolio_repo.find_portfolio_by_id(session, body.receiver_id)
            if portfolio_receiver is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Couldnt find portfolio with given id: {body.receiver_id}"
                )


            if not portfolio.coins.get(body.coin):
                raise HTTPException(status_code=404, detail=f"There is no coin with that name in your portfolio: {body.coin}")
            if portfolio.coins.get(body.coin) < body.quantity:
                raise HTTPException(status_code=400, detail=f"There is not enough quantity: {body.quantity} of coin in your portfolio: {body.coin}")
            if portfolio_receiver is None:
                raise HTTPException(status_code=404, detail=f"Couldnt find portfolio with given id: {body.receiver_id}")

            await self.trade_request_repo.create_request(
                session,
                coin=body.coin,
                quantity=body.quantity,
                coin_get=body.coin_get,
                quantity_get=body.quantity_get,
                sender_id=portfolio.id,
                receiver_id=portfolio_receiver.id,
            )

            return f"Successfully created a trade request!"





    async def _proceed_trade(self, session: AsyncSession, request, sender_portfolio, receiver_portfolio) -> None:
        """The private method used to update both sides of trade request (method used in update_user_request method below).

            Args:
                session (AsyncSession): session used in update_user_request method.
                request (TradeRequestOrm): body of the trade request.
                sender_portfolio (PortfolioOrm): portfolio of user that sent the trade request.
                receiver_portfolio (PortfolioOrm): portfolio of user that received the trade request.

            Returns:
                None
        """
        sender_coins = dict(sender_portfolio.coins or {})
        receiver_coins = dict(receiver_portfolio.coins or {})
        receiver_bought = dict(receiver_portfolio.bought_price or {})
        sender_bought = dict(sender_portfolio.bought_price or {})

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": request.coin, "vs_currencies": "usd"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            price_usd = response.json()[request.coin]["usd"]


        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": request.coin_get, "vs_currencies": "usd"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            price_usd_get = response.json()[request.coin_get]["usd"]


        sender_coins[request.coin] = sender_coins.get(request.coin, 0.0) - request.quantity
        sender_coins[request.coin_get] = sender_coins.get(request.coin_get, 0.0) + request.quantity_get

        receiver_coins[request.coin] = receiver_coins.get(request.coin, 0.0) + request.quantity
        receiver_coins[request.coin_get] = receiver_coins.get(request.coin_get, 0.0) - request.quantity_get
        if request.coin not in receiver_bought:
            receiver_bought[request.coin] = receiver_bought.get(request.coin, price_usd)
        if request.coin_get not in sender_bought:
            sender_bought[request.coin_get] = sender_bought.get(request.coin_get, price_usd_get)


        sender_portfolio.coins = sender_coins
        receiver_portfolio.coins = receiver_coins
        receiver_portfolio.bought_price = receiver_bought
        sender_portfolio.bought_price = sender_bought





    async def update_user_request(self, owner_id: UUID, accept: bool, request_id: UUID, session: AsyncSession) -> str:
        """The method conducts trade request based on accept field and request_id.

            Args:
                owner_id (UUID): The id of user.
                accept (bool): Whether to accept the trade request.
                request_id (UUID): The id of the trade request.
                session (AsyncSession): database session.

            Returns:
                str: info of transaction status.
        """

        async with session.begin():

            request = await self.trade_request_repo.find_request(session, request_id)



            sender_portfolio = await self.portfolio_repo.find_portfolio_by_id(session, request.sender_id)

            receiver_portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)

            if request.receiver_id != receiver_portfolio.id and accept:
                raise HTTPException(status_code=403, detail="This method was sent by you so you can only reject it")


            if request.status is (TradeStatus.REJECTED or TradeStatus.COMPLETED):
                raise HTTPException(status_code=404, detail="This trade has already been rejected")


            if accept:
                request.status = TradeStatus.COMPLETED
                await self._proceed_trade(
                    session=session,
                    request=request,
                    sender_portfolio=sender_portfolio,
                    receiver_portfolio=receiver_portfolio
                )

                return "trade accepted!"
            elif not accept:
                request.status = TradeStatus.REJECTED
                return "trade rejected!"


            return "error"


















