import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi import HTTPException


from src.core.domain.User import User, UserIn
from src.infrastructure.services.UserService import UserService


class UserTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.flush = AsyncMock()

    async def test_get_all_users(self):
        users = [
            User(id=uuid4(), email="igor@test.com", password="12345678"),
            User(id=uuid4(), email="igor2@test.com", password="87654321"),
        ]

        self.repository = MagicMock()
        self.repository.get_users = AsyncMock(return_value=users)

        self.service = UserService(self.repository)

        result = await self.service.get_all_users(self.session)

        self.assertEqual(users, result)
        self.assertEqual(result[0].id, users[0].id)

    async def test_user_register(self):
        user = User(id=uuid4(), email="test@igor.pl", password="")
        user_in = UserIn(email="test@igor.pl", password="")

        self.repository = MagicMock()
        self.repository.register_user = AsyncMock(return_value=user)
        self.repository.get_by_email = AsyncMock(return_value=None)

        self.service = UserService(self.repository)

        result = await self.service.register(user_in, self.session)

        self.assertEqual(result, {"id": user.id, "email": user.email})

    async def test_throws_409_when_email_already_exists_at_register(self):
        user = User(id=uuid4(), email="igor@gmail.com", password="")
        user_in = UserIn(email="test@igor.pl", password="")

        self.repository = MagicMock()
        self.repository.register_user = AsyncMock(return_value=user)
        self.repository.get_by_email = AsyncMock(return_value=user)

        self.service = UserService(self.repository)

        with self.assertRaises(HTTPException) as context:
            await self.service.register(user_in, self.session)

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(context.exception.detail, "Email already exists")

    async def test_user_login_successfully(self):
        user_id = uuid4()

        user = MagicMock()
        user.id = user_id
        user.email = "test@igor.pl"
        user.password_hash = "hashed_password"

        self.repository = MagicMock()
        self.repository.get_by_email = AsyncMock(return_value=user)

        self.service = UserService(self.repository)

        with patch(
            "src.infrastructure.services.UserService.verify_password", return_value=True
        ), patch(
            "src.infrastructure.services.UserService.generate_user_token",
            return_value={"user_token": "fake_token"},
        ):
            result = await self.service.login("test@igor.pl", "123456", self.session)

        self.assertTrue(result["access_token"] is not None)
        self.repository.get_by_email.assert_awaited_once_with(
            self.session, "test@igor.pl"
        )


    async def test_throws_401_when_password_wrong(self):
        user_id = uuid4()

        user = MagicMock()
        user.id = user_id
        user.email = "test@igor.pl"
        user.password_hash = "hashed_password"

        self.repository = MagicMock()
        self.repository.get_by_email = AsyncMock(return_value=user)

        self.service = UserService(self.repository)

        with patch("src.infrastructure.services.UserService.verify_password", return_value=False):
            with self.assertRaises(HTTPException) as context:
                await self.service.login("test@igor.pl", "wrong_password", self.session)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid credentials")




    async def test_user_login_raises_401_when_user_not_found(self):
        self.repository = MagicMock()
        self.repository.get_by_email = AsyncMock(return_value=None)

        self.service = UserService(self.repository)

        with self.assertRaises(HTTPException) as context:
            await self.service.login("test@igor.pl", "123456", self.session)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid credentials")
