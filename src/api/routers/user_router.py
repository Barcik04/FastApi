"""A module containing user endpoints."""

from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas.User import User, UserIn
from src.api.services.UserService import UserService
from src.auth.utils.deps import get_current_user_id
from src.container import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[User])
@inject
async def list_users(
    _user_id: UUID = Depends(get_current_user_id),
    service: UserService = Depends(Provide[Container.user_service]),
) -> List[User]:
    """An endpoint for getting all users.

       Args:
           _user_id (UUID): The authenticated user ID obtained from JWT.
           service (UserService, optional): The injected service dependency.

       Returns:
           List[User]: The list of all users.
       """
    return await service.get_all_users()



@router.post("/register")
@inject
async def register_user(
    user_in: UserIn,
    service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for registering a new user.

    Args:
        user_in (UserIn): The user registration input data.
        service (UserService, optional): The injected service dependency.

    Returns:
        dict: The created user model.

    Raises:
        HTTPException: 400 if email already exists.
    """
    new_user = await service.register(user_in)
    if new_user is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    return new_user




@router.post("/login")
@inject
async def login_user(
    payload: dict,
    service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for authenticating a user.

    Args:
        payload (dict): The login data containing email and password.
        service (UserService, optional): The injected service dependency.

    Returns:
        dict: The jwt token details.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    email = payload.get("email")
    password = payload.get("password")

    token = await service.login(email, password)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return token
