
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.models.PortfolioOrm import PortfolioORM
from sqlalchemy import select



class PortfolioRepository:
    async def show_user_portfolio(self, session: AsyncSession, owner_id: UUID) -> PortfolioORM:
        res = await session.execute(
            select(PortfolioORM).where(PortfolioORM.owner_id == owner_id)
        )
        return res.scalar()







