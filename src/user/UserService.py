# src/services/user_service.py

from typing import List
from src.user.UserRepository import UserRepository
from src.user.User import User, UserIn


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_in: UserIn) -> User:

        return await self.user_repo.add_user(user_in)

    async def get_all_users(self) -> List[User]:
        return await self.user_repo.get_users()
