"""Module containing portfolio abstract repository implementation."""

from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.infrastructure.models.PortfolioOrm import PortfolioOrm


class IPortfolioRepository(ABC):
    """A class representing portfolio DB repository."""

    @abstractmethod
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

    @abstractmethod
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
