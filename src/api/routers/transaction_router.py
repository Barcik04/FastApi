from datetime import datetime

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
async def show_user_portfolio(
    start_date: datetime,
    end_date: datetime,
    svc: TransactionService = Depends(get_transaction_service),
    current_user = Depends(get_current_user),
):
    user_id = _extract_user_id(current_user)
    return await svc.show_user_transactions_between_date(start_date, end_date, user_id)