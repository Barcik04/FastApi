import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.models.UserOrm import UserOrm
from src.core.domain.User import UserIn


class TestUserRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.repository = UserRepository()
        self.session = AsyncMock()

    async def test_get_by_email_found(self):
        email = "test@example.com"

        user_orm = UserOrm(
            email=email,
            password_hash="hashed_password"
        )
        user_orm.id = uuid4()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = user_orm

        self.session.execute.return_value = mock_result

        result = await self.repository.get_by_email(self.session, email)

        self.assertEqual(result, user_orm)
        self.session.execute.assert_awaited_once()

    async def test_get_by_email_not_found(self):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        self.session.execute.return_value = mock_result

        result = await self.repository.get_by_email(
            self.session,
            "missing@example.com"
        )

        self.assertIsNone(result)
        self.session.execute.assert_awaited_once()

    async def test_get_users(self):
        user_id_1 = uuid4()
        user_id_2 = uuid4()

        row_1 = MagicMock()
        row_1.id = user_id_1
        row_1.email = "user1@example.com"

        row_2 = MagicMock()
        row_2.id = user_id_2
        row_2.email = "user2@example.com"

        mock_result = MagicMock()
        mock_result.all.return_value = [row_1, row_2]

        self.session.execute.return_value = mock_result

        result = await self.repository.get_users(self.session)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].id, user_id_1)
        self.assertEqual(result[0].email, "user1@example.com")
        self.assertEqual(result[0].password, "")

        self.assertEqual(result[1].id, user_id_2)
        self.assertEqual(result[1].email, "user2@example.com")
        self.assertEqual(result[1].password, "")

        self.session.execute.assert_awaited_once()

    async def test_delete_all(self):
        await self.repository.delete_all(self.session)

        self.session.execute.assert_awaited_once()
        self.session.commit.assert_awaited_once()

