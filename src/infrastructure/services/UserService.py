"""Module containing user service implementation."""

from typing import List

from fastapi import HTTPException
from starlette import status

from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.User import User, UserIn
from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.services.IUserService import IUserService

class UserService(IUserService):
    def __init__(self, repo: UserRepository):
        self.repo = repo


    async def get_all_users(self, session: AsyncSession) -> List[User]:
        """The method for getting all users in db.

            Returns:
                List[User]: List of all users in db.
        """
        return await self.repo.get_users(session)




    async def register(self, user_in: UserIn, session: AsyncSession) -> dict:
        """Creating a user in db.

        Args:
            user_in (UserIn): body of UserIn to register.
            session (AsyncSession): DB session object.

        Returns:
            dict: body of user in db.
        """

        async with session.begin():
            existing = await self.repo.get_by_email(session, user_in.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )
            user = await self.repo.register_user(session, user_in)
            return {"id": user.id, "email": user.email}




    async def login(self, email: str, password: str, session: AsyncSession) -> dict:
        """Authenticating a user in db.

        Args:
            email (str): email address of user to login.
            password (str): password of user to login.
            session (AsyncSession): DB session object.

        Returns:
            dict: token bearer
        """

        user = await self.repo.get_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = generate_user_token(user.id)
        return {"access_token": token["user_token"], "token_type": "bearer"}
