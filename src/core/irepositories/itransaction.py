"""Module containing Transaction repository implementation."""

from datetime import datetime

from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.infrastructure.models.TransactionOrm import TransactionOrm


class ITransactionRepository(ABC):
    """A class representing trade request DB repository."""

    @abstractmethod
    async def show_user_transactions(
        self, session: AsyncSession, owner_id: UUID
    ) -> list[TransactionOrm]:
        """The method getting all transactions assigned to particular user.

        Args:
            owner_id (UUID): The id of user.
            session (AsyncSession): The database session.

        Returns:
            list[TransactionOrm]: Transactions assigned to a user.
        """

    @abstractmethod
    async def show_user_transactions_between_date(
        self,
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        owner_id: UUID,
    ) -> list[TransactionOrm]:
        """The method getting all transactions assigned to particular user between two dates.

        Args:
            owner_id (UUID): The id of user.
            session (AsyncSession): The database session.
            start_date (datetime): The start date of transactions.
            end_date (datetime): The end date of transactions.

        Returns:
            list[TransactionOrm]: Transactions assigned to a user contained between two dates.
        """

    @abstractmethod
    async def show_user_transactions_between_date_by_coin(
        self,
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        owner_id: UUID,
        coin: str,
    ) -> list[TransactionOrm]:
        """The method getting all transactions assigned to particular user between two dates grouped by coin.

        Args:
            owner_id (UUID): The id of user.
            session (AsyncSession): The database session.
            start_date (datetime): The start date of transactions.
            end_date (datetime): The end date of transactions.
            coin (str): The coin to filter transactions by.

        Returns:
            list[TransactionOrm]: Transactions assigned to a user contained between two dates.
        """
