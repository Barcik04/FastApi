# src/repositories/user_repository.py

from passlib.hash import bcrypt
from typing import List


from src.db import db
from src.user.User import User, UserIn  # your Pydantic models


class UserRepository:
    """Simple user repository with SQL queries."""

    async def add_user(self, user: UserIn) -> User:
        # Hash password before storing
        password_hash = bcrypt.hash(user.password)

        query = """
        INSERT INTO users (email, password_hash)
        VALUES ($1, $2)
        RETURNING id::text, email;
        """

        row = await db.fetchrow(query, user.email, password_hash)
        return User(id=row["id"], email=row["email"], password="")

    async def get_users(self) -> List[User]:
        query = """
        SELECT id::text AS id, email
        FROM users;
        """

        rows = await db.fetch(query)  # fetch = all rows
        return [User(id=row["id"], email=row["email"], password="") for row in rows]
