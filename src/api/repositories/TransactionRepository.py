from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select

from src.api.models.TransactionOrm import TransactionOrm


class TransactionRepository:
    async def show_user_transactions(self, session: AsyncSession, owner_id: UUID) -> list[TransactionOrm]:
        res = await session.execute(
            select(TransactionOrm).where(TransactionOrm.owner_id == owner_id)
        )
        return res.scalars().all()

    async def show_user_transactions_between_date(self, session: AsyncSession, start_date: datetime, end_date: datetime, owner_id: UUID) -> list[TransactionOrm]:
        res = await session.execute(
            select(TransactionOrm).where((TransactionOrm.owner_id == owner_id) & (TransactionOrm.date >= start_date) & (TransactionOrm.date <= end_date))
        )
        return res.scalars().all()


    async def show_user_transactions_between_date_by_coin(self, session: AsyncSession, start_date: datetime, end_date: datetime, owner_id: UUID, coin: str) -> list[TransactionOrm]:
        res = await session.execute(
            select(TransactionOrm).where((TransactionOrm.owner_id == owner_id) & (TransactionOrm.date >= start_date) & (
                        TransactionOrm.date <= end_date) & (TransactionOrm.coin == coin))
        )
        return res.scalars().all()

