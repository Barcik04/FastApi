"""Module containing User repository implementation."""

from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.UserOrm import UserOrm
from src.core.domain.User import User, UserIn


class IUserRepository(ABC):
    """A class responsible for performing user-related DB operations."""

    @abstractmethod
    async def register_user(self, session: AsyncSession, user_in: UserIn) -> User:
        """
        Create a new user and automatically create their portfolio.

        Args:
            session (AsyncSession): The database session.
            user_in (UserIn): The user registration data.

        Returns:
            User: A user representing created user.
        """


    @abstractmethod
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserOrm]:
        """
        Retrieve a user by their email.

        Args:
            session (AsyncSession): The database session.
            email (str): The email address to search for.

        Returns:
            Optional[UserOrm]: Found UserOrm, or None if not found.
        """



    @abstractmethod
    async def get_users(self, session: AsyncSession) -> List[User]:
        """
        Getting a list of all users.

        Args:
            session (AsyncSession): The database session.

        Returns:
            List[User]: A list of users.
        """

