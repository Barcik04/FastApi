# src/user/UserService.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import SessionLocal
from src.user.User import User, UserIn
from src.user.UserRepository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_in: UserIn) -> User:
        async with SessionLocal() as session:  # type: AsyncSession
            async with session.begin():
                return await self.repo.add_user(session, user_in)

    async def get_all_users(self) -> List[User]:
        async with SessionLocal() as session:
            return await self.repo.get_users(session)
