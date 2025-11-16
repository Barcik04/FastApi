"""Module containing User repository implementation."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.PortfolioOrm import PortfolioOrm
from src.api.models.UserOrm import UserORM
from src.api.schemas.User import User, UserIn
from src.auth.utils.password import hash_password


class UserRepository:
    """A class responsible for performing user-related DB operations."""

    async def register_user(self, session: AsyncSession, user_in: UserIn) -> User:
        """
        Create a new user and automatically create their portfolio.

        Args:
            session (AsyncSession): The database session.
            user_in (UserIn): The user registration data.

        Returns:
            User: A user representing created user.
        """
        user = UserORM(
            email=user_in.email,
            password_hash=hash_password(user_in.password),
        )
        session.add(user)
        await session.flush()

        session.add(PortfolioOrm(owner_id=user.id, name=f"{user.id}"))
        await session.flush()

        return User(id=user.id, email=user.email, password="")

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserORM]:
        """
        Retrieve a user by their email.

        Args:
            session (AsyncSession): The database session.
            email (str): The email address to search for.

        Returns:
            Optional[UserORM]: The matched UserORM instance, or None if not found.
        """
        res = await session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        return res.scalar_one_or_none()




    async def get_users(self, session: AsyncSession) -> List[User]:
        """
        Getting a list of all users.

        Args:
            session (AsyncSession): The database session.

        Returns:
            List[User]: A list of user containing user.
        """
        res = await session.execute(select(UserORM.id, UserORM.email))
        return [User(id=r.id, email=r.email, password="") for r in res.all()]
