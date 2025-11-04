# main.py
from fastapi import FastAPI
from src.api.routers.user_router import router as users_router
from src.user.UserRepository import UserRepository
from src.user.UserService import UserService
from src.db import init_db, close_db

from src.api.routers.auth_router import router as auth_router  # ✅ Add this


app = FastAPI(title="API")

@app.on_event("startup")
async def startup():
    await init_db()  # creates tables in dev
    app.state.user_service = UserService(UserRepository())

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(users_router)
app.include_router(auth_router)