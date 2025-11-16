# src/user/portfolio_router.py

from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse

from src.api.schemas.Portfolio import Portfolio
from src.api.services.PortfolioService import PortfolioService
from src.auth.utils.deps import get_current_user_id
from src.container import Container

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=Portfolio)
@inject
async def show_user_portfolio(
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.show_user_portfolio(user_id)


@router.post("/buy", response_class=PlainTextResponse)
@inject
async def buy_crypto(
    coin: str,
    quantity: float,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.buy_crypto(user_id, coin, quantity)


@router.post("/sell", response_class=PlainTextResponse)
@inject
async def sell_crypto(
    coin: str,
    quantity: str,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.sell_crypto(user_id, coin, quantity)


@router.post("/deposit", response_class=PlainTextResponse)
@inject
async def deposit_tether(
    quantity: float,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.deposit_tether(user_id, quantity)


@router.post("/withdraw", response_class=PlainTextResponse)
@inject
async def withdraw_tether(
    quantity: str,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.withdraw_tether(user_id, quantity)


@router.get("/p_and_l_coin", response_model=dict)
@inject
async def profit_and_loss_for_coin(
    coin: str,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.p_and_l_coin(user_id, coin)


@router.post("/transfer", response_class=PlainTextResponse)
@inject
async def transfer_coin(
    coin: str,
    quantity: str,
    transfer_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    service: PortfolioService = Depends(Provide[Container.portfolio_service]),
):
    return await service.transfer_coin(user_id, coin, quantity, transfer_id)