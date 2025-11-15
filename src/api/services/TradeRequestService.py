from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.TradeRequestOrm import TradeRequestOrm
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TradeRequestRepository import TradeRequestRepository
from uuid import UUID

from src.api.schemas.TradeRequest import TradeRequestIn, TradeStatus
from src.db import SessionLocal


class TradeRequestService:
    def __init__(self,
                 trade_request_repo: TradeRequestRepository | None = None,
                 portfolio_repo: PortfolioRepository | None = None
                 ):
        self.trade_request_repo = trade_request_repo or TradeRequestRepository()
        self.portfolio_repo = portfolio_repo or PortfolioRepository()

    async def show_user_requests(self, owner_id: UUID) -> list[TradeRequestOrm]:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)
                requests = await self.trade_request_repo.show_user_requests(session, portfolio.id)

                return requests

    async def create_user_request(self, body: TradeRequestIn, owner_id: UUID) -> str:
        async with SessionLocal() as session:
            async with session.begin():

                portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)
                if portfolio is None:
                    raise HTTPException(status_code=404, detail="Sender portfolio not found")

                portfolio_receiver = await self.portfolio_repo.find_portfolio_by_id(session, body.receiver_id)
                if portfolio_receiver is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Couldnt find portfolio with given id: {body.receiver_id}"
                    )

                coins = dict(portfolio.coins)


                if not portfolio.coins.get(body.coin):
                    raise HTTPException(status_code=400, detail=f"There is no coin with that name in your portfolio: {body.coin}")
                if portfolio.coins.get(body.coin) < body.quantity:
                    raise HTTPException(status_code=400, detail=f"There is not enough quantity: {body.quantity} of coin in your portfolio: {body.coin}")
                if portfolio_receiver is None:
                    raise HTTPException(status_code=400, detail=f"Couldnt find portfolio with given id: {body.receiver_id}")

                await self.trade_request_repo.create_request(
                    session,
                    coin=body.coin,
                    quantity=body.quantity,
                    sender_id=portfolio.id,
                    receiver_id=portfolio_receiver.id,
                )

                portfolio.coins[body.coin] = coins.get(body.coin) - body.quantity


                return f"Successfully created a trade request!"




    async def _proceed_trade(self, session: AsyncSession, request, sender_portfolio, receiver_portfolio) -> None:
        sender_coins = dict(sender_portfolio.coins or {})
        receiver_coins = dict(receiver_portfolio.coins or {})

        sender_coins[request.coin] = sender_coins.get(request.coin, 0.0) - request.quantity
        receiver_coins[request.coin] = receiver_coins.get(request.coin, 0.0) + request.quantity

        sender_portfolio.coins = sender_coins
        receiver_portfolio.coins = receiver_coins



    async def update_user_request(self, owner_id: UUID, accept: bool, request_id: UUID) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                receiver_portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)

                request = await self.trade_request_repo.find_request(session, request_id, receiver_portfolio.id)

                sender_portfolio = await self.portfolio_repo.find_portfolio_by_id(session, request.sender_id)

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


















