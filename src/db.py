# db.py
import os
import asyncpg
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise RuntimeError("DATABASE_URL not set. Check your .env path/value.")

class Database:
    pool: asyncpg.Pool | None = None

    async def connect(self):
        # e.g. postgres://user:pass@localhost:5432/mydb  (asyncpg accepts this)
        self.pool = await asyncpg.create_pool(dsn=DB_URL, min_size=1, max_size=5)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    # ---------- basic query helpers ----------
    async def execute(self, query: str, *args):
        assert self.pool, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        assert self.pool, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        assert self.pool, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        assert self.pool, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    # ---------- minimal “migration” to ensure schema ----------
    async def ensure_schema(self):
        """Create extension + users table if not exists."""
        assert self.pool, "DB pool not initialized"
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # gen_random_uuid() is available via pgcrypto on modern Postgres
                await conn.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL
                    );
                """)

db = Database()
