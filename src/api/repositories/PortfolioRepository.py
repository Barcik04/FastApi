from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.models.PortfolioOrm import PortfolioORM
from sqlalchemy import select



class PortfolioRepository:
    async def list_for_user(self, session: AsyncSession, owner_id: UUID) -> List[PortfolioORM]:
        res = await session.execute(
            select(PortfolioORM).where(PortfolioORM.owner_id == owner_id)
        )
        return list(res.scalars())


