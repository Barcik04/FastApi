# src/user/portfolio_router.py

from fastapi import APIRouter, Depends, Request, HTTPException, status
from uuid import UUID
from starlette.responses import PlainTextResponse

from src.api.schemas.Portfolio import Portfolio
from src.api.services.PortfolioService import PortfolioService
from src.auth.utils.deps import get_current_user

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    dependencies=[Depends(get_current_user)]
)

def get_portfolio_service(request: Request) -> PortfolioService:
    return request.app.state.portfolio_service

def _extract_user_id(current_user) -> UUID:
    if hasattr(current_user, "id") and current_user.id:
        return UUID(str(current_user.id))
    if isinstance(current_user, dict):
        for k in ("id", "user_id", "uid", "sub"):
            if k in current_user and current_user[k]:
                return UUID(str(current_user[k]))
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid auth payload: missing user id")

@router.get("", response_model=Portfolio)
async def show_user_portfolio(
    svc: PortfolioService = Depends(get_portfolio_service),
    current_user = Depends(get_current_user),
):
    user_id = _extract_user_id(current_user)
    return await svc.show_user_portfolio(user_id)


@router.post("/buy", response_class=PlainTextResponse)
async def buy_crypto(
    coin: str,
    quantity: float,
    svc: PortfolioService = Depends(get_portfolio_service),
    current_user = Depends(get_current_user),
):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.buy_crypto(user_id, coin, quantity)

@router.post("/sell", response_class=PlainTextResponse)
async def sell_crypto(
        coin: str,
        quantity: str,
        svc: PortfolioService = Depends(get_portfolio_service),
        current_user = Depends(get_current_user),
):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.sell_crypto(user_id, coin, quantity)

@router.post("/deposit", response_class=PlainTextResponse)
async def deposit_theter(
        quantity: float,
        svc: PortfolioService = Depends(get_portfolio_service),
        current_user = Depends(get_current_user),
):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.deposit_tether(user_id, quantity)