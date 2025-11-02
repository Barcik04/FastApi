# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.user.UserController import router as users_router
from src.user.UserRepository import UserRepository
from src.user.UserService import UserService
from src.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db.connect()
    repo = UserRepository()
    app.state.user_service = UserService(repo)   # attach service here
    try:
        yield
    finally:
        # shutdown
        await db.disconnect()

app = FastAPI(title="API", lifespan=lifespan)

# routes
app.include_router(users_router)

