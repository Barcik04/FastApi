# src/user/UserRepository.py
from typing import List
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.User import User, UserIn
from src.user.user_model import UserORM

class UserRepository:
    async def add_user(self, session: AsyncSession, user_in: UserIn) -> User:
        entity = UserORM(
            email=user_in.email,
            password_hash=bcrypt.hash(user_in.password),
        )
        session.add(entity)
        await session.flush()      # get PK
        await session.refresh(entity)
        return User(id=entity.id, email=entity.email, password="")

    async def get_users(self, session: AsyncSession) -> List[User]:
        stmt = select(UserORM.id, UserORM.email)
        res = await session.execute(stmt)
        rows = res.all()
        return [User(id=r.id, email=r.email, password="") for r in rows]
