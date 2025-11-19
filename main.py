"""Main module of the app."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.cors import CORSMiddleware

from src.api.routers.portfolio_router import router as portfolio_router
from src.api.routers.trade_request_router import router as trade_request_router
from src.api.routers.transaction_router import router as transaction_router
from src.api.routers.user_router import router as users_router
from src.container import Container
from src.db import init_db, close_db


container = Container()
container.wire(modules=[
    "src.api.routers.portfolio_router",
    "src.api.routers.trade_request_router",
    "src.api.routers.transaction_router",
    "src.api.routers.user_router",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup/shutdown."""
    await init_db()
    try:
        yield
    finally:
        await close_db()


app = FastAPI(title="API", lifespan=lifespan)



app.include_router(users_router)
app.include_router(portfolio_router)
app.include_router(transaction_router)
app.include_router(trade_request_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)




### FRONTEND CORS CONFIG
origins = [
    "http://localhost:63342",
    "http://127.0.0.1:63342",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)