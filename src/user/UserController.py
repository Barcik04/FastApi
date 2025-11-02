from fastapi import APIRouter, Depends, Request
from src.user.User import UserIn
from src.user.UserService import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service

@router.post("")
async def create_user(user_in: UserIn, svc: UserService = Depends(get_user_service)):
    return await svc.create_user(user_in)

@router.get("")
async def list_users(svc: UserService = Depends(get_user_service)):
    return await svc.get_all_users()
