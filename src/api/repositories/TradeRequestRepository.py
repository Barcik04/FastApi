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

    async def create_request(self, session: AsyncSession, coin: str, quantity: float, sender_id: UUID, receiver_id: UUID) -> TradeRequestOrm:
        obj = TradeRequestOrm(
            sender_id=sender_id,
            receiver_id=receiver_id,
            coin=coin,
            quantity=quantity,
        )
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj
