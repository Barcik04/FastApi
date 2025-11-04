# src/user/user_router.py
from fastapi import APIRouter, Depends, Request
from typing import List
from src.api.schemas.User import User
from src.api.services.UserService import UserService
from src.auth.utils.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])

def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


@router.get("", response_model=List[User])
async def list_users(svc: UserService = Depends(get_user_service)):
    return await svc.get_all_users()
