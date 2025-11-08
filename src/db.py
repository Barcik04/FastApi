# src/db.py
import os
import asyncio
from contextlib import asynccontextmanager

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError  # generic SA errors

load_dotenv(find_dotenv())

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL or "+asyncpg" not in DB_URL:
    raise RuntimeError("DATABASE_URL must be like postgresql+asyncpg://user:pass@host:5432/dbname")

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DB_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



async def init_db(retries: int = 5, delay: int = 5) -> None:

    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            return
        except SQLAlchemyError as e:
            print(f"[DB] Attempt {attempt}/{retries} failed: {e}")
            if attempt == retries:
                raise
            await asyncio.sleep(delay)

async def close_db():
    await engine.dispose()

@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise