from fastapi import HTTPException

from src.api.models.TradeRequestOrm import TradeRequestOrm
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TradeRequestRepository import TradeRequestRepository
from uuid import UUID

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
                requests = await self.trade_request_repo.show_user_requests(session, owner_id)

                return requests

    async def create_user_request(self, coin: str, quantity: float, owner_id: UUID, receiver_id: UUID) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)
                portfolio_receiver = await self.portfolio_repo.find_portfolio_by_id(session, receiver_id)

                if not portfolio.coins.get(coin):
                    raise HTTPException(status_code=400, detail=f"There is no coin with that name in your portfolio: {coin}")
                if portfolio.coins.get(coin) > quantity:
                    raise HTTPException(status_code=400, detail=f"There is not enough quantity: {quantity} of coin in your portfolio: {coin}")
                if portfolio_receiver is None:
                    raise HTTPException(status_code=400, detail=f"Couldnt find portfolio with given id: {receiver_id}")

                tr = TradeRequestOrm(
                    coin=coin,
                    quantity=quantity,
                    receiver_id=receiver_id,
                )
                session.add(tr)

                return f"Successfully created a trade request!"







