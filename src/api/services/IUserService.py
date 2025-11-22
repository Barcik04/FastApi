from abc import ABC, abstractmethod
from typing import List

from src.api.schemas.User import User, UserIn


class IUserService(ABC):
    """An abstract base class representing a user service."""

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """Method to return all users.

        Returns:
            List[User]: List of all users.
        """

    @abstractmethod
    async def register(self, user_in: UserIn) -> dict:
        """Method to create new user in db.

        Args:
            user_in (UserIn): DTO of user to register.

        Returns:
            dict: body of user in db.
        """

    @abstractmethod
    async def login(self, email: str, password: str) -> dict:
        """Method to login user and create JWT token.

        Args:
            email : email of user to login.
            password : password of user to login.

        Returns:
            dict: body with a token and token's type.
        """