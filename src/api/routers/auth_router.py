"""A module containing continent endpoints."""


from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.schemas.User import UserIn
from src.auth.AuthService import AuthService
from src.container import Container
from src.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["auth"])


async def session_dep():
    async with SessionLocal() as s:
        async with s.begin():
            yield s


@router.post("/register")
@inject
async def register(
    user_in: UserIn,
    session=Depends(session_dep),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.register(session, user_in)


@router.post("/login")
@inject
async def login(
    payload: dict,
    session=Depends(session_dep),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.login(session, payload["email"], payload["password"])
