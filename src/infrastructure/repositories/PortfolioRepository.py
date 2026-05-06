"""Module containing portfolio repository implementation."""

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.irepositories.iportfolio import IPortfolioRepository
from src.infrastructure.models.PortfolioOrm import PortfolioOrm
from sqlalchemy import select


class PortfolioRepository(IPortfolioRepository):
    """A class representing portfolio DB repository."""

    async def show_user_portfolio(
        self, session: AsyncSession, owner_id: UUID
    ) -> PortfolioOrm:
        """The method finds user's portfolio from the data storage.

        Args:
            owner_id (UUID): The id of the user.
            session (AsyncSession): The database session.

        Returns:
            PortfolioOrm: found Portfolio in the data storage.
        """
        res = await session.execute(
            select(PortfolioOrm).where(PortfolioOrm.owner_id == owner_id)
        )
        return res.scalar()

    async def find_portfolio_by_id(
        self, session: AsyncSession, portfolio_id: UUID
    ) -> PortfolioOrm:
        """The method finds portfolio from the data storage by given portfolio ID.

        Args:
            portfolio_id (UUID): The id of the portfolio.
            session (AsyncSession): The database session.

        Returns:
            PortfolioOrm: found Portfolio in the data storage.
        """
        res = await session.execute(
            select(PortfolioOrm).where(PortfolioOrm.id == portfolio_id)
        )
        return res.scalar()
