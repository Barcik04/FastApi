# src/user/UserRepository.py
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.user.UserOrm import UserORM
from src.core.domain.User import User, UserIn

class UserRepository:
    async def register_user(self, session: AsyncSession, user_in: UserIn) -> User:
        entity = UserORM(email=user_in.email, password_hash=user_in.password)
        session.add(entity)
        await session.flush()
        await session.refresh(entity)
        return User(id=entity.id, email=entity.email, password="")

    async def get_by_uuid(self, session: AsyncSession, uuid) -> Optional[UserORM]:
        res = await session.execute(select(UserORM).where(UserORM.id == uuid))
        return res.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserORM]:
        res = await session.execute(select(UserORM).where(UserORM.email == email))
        return res.scalar_one_or_none()

    async def get_users(self, session: AsyncSession) -> List[User]:
        res = await session.execute(select(UserORM.id, UserORM.email))
        return [User(id=r.id, email=r.email, password="") for r in res.all()]
