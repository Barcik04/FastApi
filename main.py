from fastapi import FastAPI
from src.user.UserController import router as users_router
from src.user.UserRepository import UserRepository
from src.user.UserService import UserService
from src.db import db

app = FastAPI(title="API")

@app.on_event("startup")
async def startup():
    await db.connect()
    repo = UserRepository()
    app.state.user_service = UserService(repo)

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.include_router(users_router)
