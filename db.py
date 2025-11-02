# db.py (wherever it lives: root or src/)
import os
import asyncpg
from dotenv import load_dotenv, find_dotenv

# auto-discover .env starting from CWD and walking up
load_dotenv(find_dotenv())

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise RuntimeError("DATABASE_URL not set. Check your .env path/value.")

class Database:
    pool: asyncpg.Pool | None = None

    async def connect(self):
        print(f"[DB] Connecting to: {DB_URL}")  # optional debug
        self.pool = await asyncpg.create_pool(dsn=DB_URL, min_size=1, max_size=5)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def fetchval(self, query: str):
        assert self.pool is not None, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query)

db = Database()
