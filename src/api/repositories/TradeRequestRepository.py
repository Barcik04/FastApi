from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select

from src.api.models.TradeRequestOrm import TradeRequestOrm


class TradeRequestRepository:
    async def show_user_requests(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        res = await session.execute(
            select(TradeRequestOrm).where(TradeRequestOrm.receiver_id==owner_id or TradeRequestOrm.sender_id==owner_id)
        )
        return res.scalars().all()

    async def show_user_senders(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        res = await session.execute(
            select(TradeRequestOrm).where(TradeRequestOrm.sender_id==owner_id)
        )

        return res.scalars().all()

    async def show_user_receivers(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        res = await session.execute(
            select(TradeRequestOrm).where(TradeRequestOrm.receiver_id==owner_id)
        )

        return res.scalars().all()