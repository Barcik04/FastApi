"""Module containing Transaction repository implementation."""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select

from src.api.models.TransactionOrm import TransactionOrm


class TransactionRepository:
    """A class representing trade request DB repository."""

    async def show_user_transactions(self, session: AsyncSession, owner_id: UUID) -> list[TransactionOrm]:
        """The method getting all transactions assigned to particular user.

                   Args:
                       owner_id (UUID): The id of user.
                       session (AsyncSession): The database session.

                   Returns:
                       list[TransactionOrm]: Transactions assigned to a user.
               """
        res = await session.execute(
            select(TransactionOrm).where(TransactionOrm.owner_id == owner_id)
        )
        return res.scalars().all()




    async def show_user_transactions_between_date(self, session: AsyncSession, start_date: datetime, end_date: datetime, owner_id: UUID) -> list[TransactionOrm]:
        """The method getting all transactions assigned to particular user between two dates.

                     Args:
                         owner_id (UUID): The id of user.
                         session (AsyncSession): The database session.
                         start_date (datetime): The start date of transactions.
                         end_date (datetime): The end date of transactions.

                     Returns:
                         list[TransactionOrm]: Transactions assigned to a user contained between two dates.
                 """
        res = await session.execute(
            select(TransactionOrm).where((TransactionOrm.owner_id == owner_id) & (TransactionOrm.date >= start_date) & (TransactionOrm.date <= end_date))
        )
        return res.scalars().all()





    async def show_user_transactions_between_date_by_coin(self, session: AsyncSession, start_date: datetime, end_date: datetime, owner_id: UUID, coin: str) -> list[TransactionOrm]:
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
        res = await session.execute(
            select(TransactionOrm).where((TransactionOrm.owner_id == owner_id) & (TransactionOrm.date >= start_date) & (
                        TransactionOrm.date <= end_date) & (TransactionOrm.coin == coin))
        )
        return res.scalars().all()

