from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette import status

from src.api.schemas.CryptoData import CryptoData
from src.api.services.CryptoDataService import CryptoDataService
from src.auth.utils.deps import get_current_user


router = APIRouter(prefix="/crypto-data", tags=["crypto-data"], dependencies=[Depends(get_current_user)])


def get_crypto_data_service(request: Request) -> CryptoDataService:
    return request.app.state.crypto_data_service


def _extract_user_id(current_user) -> UUID:
    if hasattr(current_user, "id") and current_user.id:
        return UUID(str(current_user.id))
    if isinstance(current_user, dict):
        for k in ("id", "user_id", "uid", "sub"):
            if k in current_user and current_user[k]:
                return UUID(str(current_user[k]))
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid auth payload: missing user id")


@router.get("", response_model=List[CryptoData])
async def list_crypto_data(
    svc: CryptoDataService = Depends(get_crypto_data_service),
    current_user = Depends(get_current_user),
):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.list_for_user(user_id)


@router.get("/amount_graph", response_model=None)
async def list_of_amount_for_user(
    mode: int,
    svc: CryptoDataService = Depends(get_crypto_data_service),
    current_user = Depends(get_current_user),
):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.list_of_amount_for_user(user_id, mode)


@router.get("/24h", response_model=None)
async def graph_portfolio_val(
    days: int,
    svc: CryptoDataService = Depends(get_crypto_data_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_portfolio_val(user_id, days)


@router.get("/sep-coins", response_model=None)
async def graph_multiple_coins(
    days: int,
    svc: CryptoDataService = Depends(get_crypto_data_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_multiple_coins(user_id, days)


@router.get("/p_n_l_perc", response_model=None)
async def graph_p_n_l_percent(
    svc: CryptoDataService = Depends(get_crypto_data_service),
    current_user=Depends(get_current_user),

):
    user_id: UUID = _extract_user_id(current_user)
    return await svc.graph_p_n_l_percent(user_id)