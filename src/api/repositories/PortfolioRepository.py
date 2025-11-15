
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.models.PortfolioOrm import PortfolioOrm
from sqlalchemy import select



class PortfolioRepository:
    async def show_user_portfolio(self, session: AsyncSession, owner_id: UUID) -> PortfolioOrm:
        res = await session.execute(
            select(PortfolioOrm).where(PortfolioOrm.owner_id == owner_id)
        )
        return res.scalar()

    async def find_portfolio_by_id(self, session: AsyncSession, portfolio_id: UUID) -> PortfolioOrm:
        res = await session.execute(
            select(PortfolioOrm).where(PortfolioOrm.id == portfolio_id)
        )
        return res.scalar()







