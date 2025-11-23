from abc import ABC, abstractmethod
from uuid import UUID

from src.api.models.PortfolioOrm import PortfolioOrm
from sqlalchemy.ext.asyncio import AsyncSession


class IPortfolioService(ABC):
    """An abstract base class representing a portfolio service."""


    @abstractmethod
    async def show_user_portfolio(self, owner_id: UUID, session: AsyncSession) -> PortfolioOrm:
         """Get user's portfolio.

        Args:
            owner_id (UUID): The id of the user.
            session (AsyncSession): The database session.

        Returns:
            PortfolioOrm: Portfolio assigned to the user.
        """

    @abstractmethod
    async def buy_crypto(self, owner_id: UUID, coin: str, quantity: float, session: AsyncSession) -> str:
         """Method for adding (buying) crypto to user's portfolio.

        Args:
            owner_id (UUID): The id of the user.
            coin: The name of the coin to buy.
            quantity: The quantity of the coin to buy.
            session (AsyncSession): The database session.

        Returns:
            str: Information of transaction status
        """

    @abstractmethod
    async def sell_crypto(self, owner_id: UUID, coin: str, quantity: str, session: AsyncSession) -> str:
        """Method for removing (selling) crypto to user's portfolio.


        Args:
            owner_id (UUID): The id of the user.
            coin: The name of the coin to sell.
            quantity: The quantity of the coin to sell.
            session (AsyncSession): The database session.

        Returns:
            str: Information of transaction status.
        """

    @abstractmethod
    async def deposit_tether(self, owner_id: UUID, quantity: float, session: AsyncSession) -> str:
        """Method for adding (depositing) tether to user's portfolio.


        Args:
            owner_id (UUID): The id of the user.
            quantity: The quantity of tether to deposit.
            session (AsyncSession): The database session.

        Returns:
            str: Information of transaction status.
        """

    @abstractmethod
    async def withdraw_tether(self, owner_id: UUID, quantity: str, session: AsyncSession) -> str:
        """Method for withdrawing tether to users bank account.


        Args:
            owner_id (UUID): The id of the user.
            quantity: The quantity of the coin to withdraw.
            session (AsyncSession) : The database session.

        Returns:
            str: Information of transaction status.
        """

    @abstractmethod
    async def p_and_l_coin(self, owner_id: UUID, coin: str, session: AsyncSession) -> dict[str, float]:
        """Method for displaying profit and losses for specified coin in portfolio.


        Args:
            owner_id (UUID): The id of the user.
            coin: The name of the coin display p_n_l for.
            session (AsyncSession) : The database session.

        Returns:
            dict[str, float]: Profit and losses for specified coin.
        """

    @abstractmethod
    async def transfer_coin(self, owner_id: UUID, coin: str, quantity: str, transfer_id: UUID, session: AsyncSession) -> str:
        """Method for transferring a coin from user's portfolio to specified portfolio.


        Args:
            owner_id (UUID): The id of the user.
            coin: The name of the coin to transfer.
            quantity: The quantity of the coin to transfer.
            transfer_id: The id of the portfolio to transfer coin to.
            session (AsyncSession): The database session.

        Returns:
            str: Information of transaction status.
        """