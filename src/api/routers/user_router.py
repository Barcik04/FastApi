# src/user/user_router.py
from fastapi import APIRouter, Depends, Request
from typing import List
from src.core.domain.User import UserIn, User
from src.user.UserService import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service

@router.post("", response_model=User)
async def create_user(user_in: UserIn, svc: UserService = Depends(get_user_service)):
    return await svc.create_user(user_in)

@router.get("", response_model=List[User])
async def list_users(svc: UserService = Depends(get_user_service)):
    return await svc.get_all_users()
