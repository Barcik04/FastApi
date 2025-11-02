# create_schema.py
import asyncio
from db import db

DDL = """
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

async def main():
    await db.connect()
    try:
        await db.execute(DDL)
        print("[DB] users table ready.")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
