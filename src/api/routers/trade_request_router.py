"""A module containing trade request endpoints."""


from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.ITradeRequestService import ITradeRequestService
from src.db import get_session


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
    session: AsyncSession = Depends(get_session),
    service: ITradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    """An endpoint for retrieving all trade requests involving user.

       Args:
           user_id (UUID): The authenticated user's ID fetched from the JWT.
           service (ITradeRequestService, optional): The injected service dependency.
           session (AsyncSession): The database session.

       Returns:
           list[TradeRequest]: The list of trade requests for the user.
       """
    return await service.show_user_requests(user_id, session)


@router.post("/send", response_model=str)
@inject
async def create_user_request(
    body: TradeRequestIn,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    """An endpoint for creating a new trade request.

      Args:
          body (TradeRequestIn): The trade request body with trade details.
          user_id (UUID): The authenticated user's ID fetched from the JWT token.
          service (ITradeRequestService, optional): The injected service dependency.
          session (AsyncSession): The database session.

      Returns:
          str: A confirmation message.

    """
    return await service.create_user_request(body, user_id, session)


@router.put("/update", response_model=str)
@inject
async def update_user_request(
    body: TradeRequestUpdateDto,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITradeRequestService = Depends(Provide[Container.trade_request_service]),
):
    """An endpoint for updating the status of a trade request.

       Args:
           body (TradeRequestUpdateDto): The update payload containing acceptance bool and request_id.
           user_id (UUID): The authenticated user's ID fetched from the JWT token.
           service (ITradeRequestService, optional): The injected trade request service dependency.
           session (AsyncSession): The database session.

       Returns:
           str: A confirmation message.
    """
    return await service.update_user_request(user_id, body.accept, body.request_id, session)
