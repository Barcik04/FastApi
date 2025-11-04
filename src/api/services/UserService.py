# src/user/UserService.py
from typing import List
from src.db import SessionLocal
from src.api.schemas.User import User, UserIn
from src.api.repositories.UserRepository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo


    async def get_all_users(self) -> List[User]:
        async with SessionLocal() as session:
            return await self.repo.get_users(session)
