# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TradeRequestRepository import TradeRequestRepository
from src.api.routers.user_router import router as users_router
from src.api.repositories.UserRepository import UserRepository
from src.api.services.PortfolioService import PortfolioService
from src.api.services.TradeRequestService import TradeRequestService
from src.api.services.TransactionService import TransactionService
from src.api.repositories.TransactionRepository import TransactionRepository
from src.api.services.UserService import UserService
from src.db import init_db, close_db
from src.api.routers.portfolio_router import router as portfolio_router
from src.api.routers.auth_router import router as auth_router
from src.api.routers.transaction_router import router as transaction_router
from src.api.routers.trade_request_router import router as trade_request_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.user_service = UserService(UserRepository())
    app.state.portfolio_service = PortfolioService(PortfolioRepository())
    app.state.transaction_service = TransactionService(TransactionRepository())
    app.state.trade_request_service = TradeRequestService(TradeRequestRepository())
    try:
        yield
    finally:
        await close_db()

app = FastAPI(title="API", lifespan=lifespan)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(transaction_router)
app.include_router(trade_request_router)