from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.User import User, UserIn


class IUserService(ABC):
    """An abstract base class representing a user service."""

    @abstractmethod
    async def get_all_users(self, session: AsyncSession) -> List[User]:
        """Method to return all users.

        Returns:
            List[User]: List of all users.
        """

    @abstractmethod
    async def register(self, user_in: UserIn, session: AsyncSession) -> dict:
        """Method to create new user in db.

        Args:
            user_in (UserIn): DTO of user to register.
            session (AsyncSession): DB session object.

        Returns:
            dict: body of user in db.
        """

    @abstractmethod
    async def login(self, email: str, password: str, session: AsyncSession) -> dict:
        """Method to login user and create JWT token.

        Args:
            email : email of user to login.
            password : password of user to login.
            session (AsyncSession): DB session object.

        Returns:
            dict: body with a token and token's type.
        """
