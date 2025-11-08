# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.routers import crypto_data_router
from src.api.routers.user_router import router as users_router
from src.api.repositories.UserRepository import UserRepository
from src.api.services.CryptoDataService import CryptoDataService
from src.api.services.PortfolioService import PortfolioService
from src.api.services.UserService import UserService
from src.db import init_db, close_db

from src.api.routers.portfolio_router import router as portfolio_router
from src.api.routers.auth_router import router as auth_router
from src.api.routers.crypto_data_router import router as crypto_data_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.user_service = UserService(UserRepository())
    app.state.portfolio_service = PortfolioService(PortfolioRepository())
    app.state.crypto_data_service = CryptoDataService()
    try:
        yield
    finally:
        await close_db()

app = FastAPI(title="API", lifespan=lifespan)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(crypto_data_router)