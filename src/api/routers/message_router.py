"""A module containing message endpoints."""

from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.Message import Message, MessageIn
from src.container import Container
from src.db import get_session
from src.infrastructure.services.IMessageService import IMessageService
from src.infrastructure.utils.deps import get_current_user_id

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[Message])
@inject
async def show_user_messages(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IMessageService = Depends(Provide[Container.message_service]),
):
    """An endpoint for fetching all messages for user."""

    return await service.show_user_messages(user_id, session)


@router.post("/send", response_model=Message)
@inject
async def send_message(
    body: MessageIn,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IMessageService = Depends(Provide[Container.message_service]),
):
    """An endpoint for sending a message to another user."""

    return await service.send_message(body, user_id, session)
