# src/user/AuthService.py
from fastapi import HTTPException, status
from src.auth.utils.password import verify_password
from src.auth.utils.token import generate_user_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.repositories import UserRepository

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, session: AsyncSession, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        tok = generate_user_token(user.id)
        return {"access_token": tok["user_token"], "token_type": "bearer"}

    async def register(self, session: AsyncSession, user_in) -> dict:
        user = await self.repo.register_user(session, user_in)
        if user is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        return {"id": user.id, "email": user.email}
