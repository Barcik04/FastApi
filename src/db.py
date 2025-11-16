# src/db.py
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


load_dotenv(find_dotenv())

DB_URL = os.getenv("DATABASE_URL")

class Base(DeclarativeBase):
    pass


engine = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()


@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        yield session
        await session.commit()
