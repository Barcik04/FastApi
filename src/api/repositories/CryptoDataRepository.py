from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.CryptoDataOrm import CryptoDataOrm


class CryptoDataRepository:
    async def show_user_data(self, session: AsyncSession, owner_id: UUID) -> list[CryptoDataOrm]:
        res = await session.execute(
            select(CryptoDataOrm).where(CryptoDataOrm.owner_id == owner_id)
        )
        return res.scalars().all()