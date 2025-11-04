# src/user/UserService.py
from typing import List
from fastapi import HTTPException, status
from src.db import SessionLocal
from src.core.domain.User import User, UserIn
from src.user.UserRepository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_in: UserIn) -> User:
        async with SessionLocal() as session:
            async with session.begin():
                if await self.repo.get_by_email(session, user_in.email):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Email already exists")
                return await self.repo.add_user(session, user_in)

    async def get_all_users(self) -> List[User]:
        async with SessionLocal() as session:
            return await self.repo.get_users(session)
