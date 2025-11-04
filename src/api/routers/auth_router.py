# src/user/AuthController.py
from fastapi import APIRouter, Depends, Request
from src.db import SessionLocal
from src.auth.AuthService import AuthService
from src.user.UserRepository import UserRepository
from src.core.domain.User import UserIn

router = APIRouter(prefix="/auth", tags=["auth"])
repo = UserRepository()
auth = AuthService(repo)

async def session_dep():
    async with SessionLocal() as s:
        async with s.begin():
            yield s

@router.post("/register")
async def register(user_in: UserIn, session = Depends(session_dep)):
    return await auth.register(session, user_in)

@router.post("/login")
async def login(payload: dict, session = Depends(session_dep)):
    return await auth.login(session, payload["email"], payload["password"])
