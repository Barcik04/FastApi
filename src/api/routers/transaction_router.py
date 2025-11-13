
from fastapi import APIRouter, Depends, Request, HTTPException, status
from uuid import UUID

from src.api.schemas.Transaction import Transaction
from src.api.services.TransactionService import TransactionService
from src.auth.utils.deps import get_current_user


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_user)]
)

def get_transaction_service(request: Request) -> TransactionService:
    return request.app.state.transaction_service

def _extract_user_id(current_user) -> UUID:
    if hasattr(current_user, "id") and current_user.id:
        return UUID(str(current_user.id))
    if isinstance(current_user, dict):
        for k in ("id", "user_id", "uid", "sub"):
            if k in current_user and current_user[k]:
                return UUID(str(current_user[k]))
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid auth payload: missing user id")


@router.get("/between", response_model=list[Transaction])
async def show_user_transactions(

    svc: TransactionService = Depends(get_transaction_service),
    current_user = Depends(get_current_user),
):
    user_id = _extract_user_id(current_user)
    return await svc.show_user_transactions(user_id)


@router.get("/val", response_model=None)
async def graph_portfolio_val(
    days: int,
    svc: TransactionService = Depends(get_transaction_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_portfolio_val(user_id, days)


@router.get("/sep-coins", response_model=None)
async def graph_multiple_coins(
    days: int,
    svc: TransactionService = Depends(get_transaction_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_multiple_coins(user_id, days)


@router.get("/p_n_l_perc", response_model=None)
async def graph_p_n_l_percent(
    svc: TransactionService = Depends(get_transaction_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_p_n_l_percent(user_id)


@router.get("/p_n_l", response_model=None)
async def graph_p_n_l(
    svc: TransactionService = Depends(get_transaction_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_p_n_l(user_id)