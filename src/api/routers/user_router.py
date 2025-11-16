# src/user/user_router.py

from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.schemas.User import User
from src.api.services.UserService import UserService
from src.auth.utils.deps import get_current_user_id
from src.container import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[User])
@inject
async def list_users(
    _user_id: UUID = Depends(get_current_user_id),
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.get_all_users()
