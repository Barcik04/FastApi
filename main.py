# main.py
from fastapi import FastAPI

from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.routers.user_router import router as users_router
from src.api.repositories.UserRepository import UserRepository
from src.api.services.PortfolioService import PortfolioService
from src.api.services.UserService import UserService
from src.db import init_db, close_db


from src.api.routers.portfolio_router import router as portfolio_router
from src.api.routers.auth_router import router as auth_router


app = FastAPI(title="API")

@app.on_event("startup")
async def startup():
    await init_db()  # creates tables in dev
    app.state.user_service = UserService(UserRepository())
    app.state.portfolio_service = PortfolioService(PortfolioRepository())

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(portfolio_router)