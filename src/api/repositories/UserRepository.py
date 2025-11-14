# src/user/UserRepository.py
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.PortfolioOrm import PortfolioOrm
from src.api.models.UserOrm import UserORM
from src.api.schemas.User import User, UserIn
from src.auth.utils.password import hash_password


class UserRepository:
    async def register_user(self, session: AsyncSession, user_in: UserIn) -> User:
        user = UserORM(email=user_in.email, password_hash=hash_password(user_in.password),)
        session.add(user)
        await session.flush()

        session.add(PortfolioOrm(owner_id=user.id, name=f"Portfolio {user.id}"))
        await session.flush()

        return User(id=user.id, email=user.email, password="")

    async def get_by_uuid(self, session: AsyncSession, uuid) -> Optional[UserORM]:
        res = await session.execute(select(UserORM).where(UserORM.id == uuid))
        return res.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserORM]:
        res = await session.execute(select(UserORM).where(UserORM.email == email))
        return res.scalar_one_or_none()

    async def get_users(self, session: AsyncSession) -> List[User]:
        res = await session.execute(select(UserORM.id, UserORM.email))
        return [User(id=r.id, email=r.email, password="") for r in res.all()]
