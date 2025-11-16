from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.schemas.TradeRequest import (
    TradeRequest,
    TradeRequestIn,
    TradeRequestUpdateDto,
)
from src.api.services.TradeRequestService import TradeRequestService
from src.auth.utils.deps import get_current_user_id
from src.container import Container


router = APIRouter(prefix="/trade_requests", tags=["trade_requests"])


@router.get("", response_model=list[TradeRequest])
@inject
async def show_user_requests(
    user_id: UUID = Depends(get_current_user_id),
    service: TradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    return await service.show_user_requests(user_id)


@router.post("/send", response_model=str)
@inject
async def create_user_request(
    body: TradeRequestIn,
    user_id: UUID = Depends(get_current_user_id),
    service: TradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    return await service.create_user_request(body, user_id)


@router.put("/update", response_model=str)
@inject
async def update_user_request(
    body: TradeRequestUpdateDto,
    user_id: UUID = Depends(get_current_user_id),
    service: TradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    return await service.update_user_request(user_id, body.accept, body.request_id)
