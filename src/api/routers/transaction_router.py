from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.schemas.Transaction import Transaction
from src.api.services.TransactionService import TransactionService
from src.auth.utils.deps import get_current_user_id
from src.container import Container


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[Transaction])
@inject
async def list_for_user(
    user_id: UUID = Depends(get_current_user_id),
    service: TransactionService = Depends(Provide[Container.transaction_service]),
):
    return await service.list_for_user(user_id)


@router.get("/val", response_model=None)
@inject
async def graph_portfolio_val(
    days: int,
    user_id: UUID = Depends(get_current_user_id),
    service: TransactionService = Depends(Provide[Container.transaction_service]),
):
    return await service.graph_portfolio_val(user_id, days)


@router.get("/sep-coins", response_model=None)
@inject
async def graph_multiple_coins(
    days: int,
    user_id: UUID = Depends(get_current_user_id),
    service: TransactionService = Depends(Provide[Container.transaction_service]),
):
    return await service.graph_multiple_coins(user_id, days)


@router.get("/p_n_l_perc", response_model=None)
@inject
async def graph_p_n_l_percent(
    user_id: UUID = Depends(get_current_user_id),
    service: TransactionService = Depends(Provide[Container.transaction_service]),
):
    return await service.graph_p_n_l_percent(user_id)


@router.get("/p_n_l", response_model=None)
@inject
async def graph_p_n_l(
    user_id: UUID = Depends(get_current_user_id),
    service: TransactionService = Depends(Provide[Container.transaction_service]),
):
    return await service.graph_p_n_l(user_id)