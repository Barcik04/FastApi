"""Module containing User repository implementation."""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.irepositories.iuser import IUserRepository
from src.infrastructure.models.PortfolioOrm import PortfolioOrm
from src.infrastructure.models.UserOrm import UserOrm
from src.core.domain.User import User, UserIn
from src.infrastructure.utils.password import hash_password


class UserRepository(IUserRepository):
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
        user = UserOrm(
            email=user_in.email,
            password_hash=hash_password(user_in.password),
        )
        session.add(user)
        await session.flush()

        session.add(PortfolioOrm(owner_id=user.id, name=f"{user.id}"))
        await session.flush()

        return User(id=user.id, email=user.email, password="")

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> Optional[UserOrm]:
        """
        Retrieve a user by their email.

        Args:
            session (AsyncSession): The database session.
            email (str): The email address to search for.

        Returns:
            Optional[UserOrm]: Found UserOrm, or None if not found.
        """
        res = await session.execute(select(UserOrm).where(UserOrm.email == email))
        return res.scalar_one_or_none()

    async def get_users(self, session: AsyncSession) -> List[User]:
        """
        Getting a list of all users.

        Args:
            session (AsyncSession): The database session.

        Returns:
            List[User]: A list of users.
        """
        res = await session.execute(select(UserOrm.id, UserOrm.email))
        return [User(id=r.id, email=r.email, password="") for r in res.all()]

    async def delete_all(self, session: AsyncSession) -> None:
        await session.execute(delete(UserOrm))
        await session.commit()
