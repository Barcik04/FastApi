from abc import ABC, abstractmethod
from uuid import UUID

from src.api.models.TransactionOrm import TransactionOrm


class ITransactionService(ABC):
    """An abstract base class representing a transaction service."""

    @abstractmethod
    async def list_for_user(self, owner_id: UUID) -> list[TransactionOrm]:
        """Method to list all transactions associated with a user.

        Args:
            owner_id (UUID): user's id.

        Returns:
            List[TransactionOrm]: list of transactions associated with a user.
        """

    @abstractmethod
    async def graph_portfolio_val(self, owner_id: UUID, days: int) -> None:
        """Method to display a graph presenting value of user's portfolio over time with specified amount of days in the past.

        Args:
            owner_id (UUID): user's id.
            days (int): amount of days in the past.

        Returns:
            None
        """

    @abstractmethod
    async def graph_multiple_coins(self, owner_id: UUID, days: int) -> None:
        """Method to display a graph presenting value of each coin in user's portfolio over time with specified amount of days in the past.

        Args:
            owner_id (UUID): user's id.
            days (int): amount of days in the past.

        Returns:
            None
        """

    @abstractmethod
    async def graph_p_n_l_percent(self, owner_id: UUID) -> None:
        """Method to display profit and loss graph counting from the first transaction associated with user's portfolio in %.

        Args:
            owner_id (UUID): user's id.

        Returns:
            None
        """

    @abstractmethod
    async def graph_p_n_l(self, owner_id: UUID) -> None:
        """Method to display profit and loss graph counting from the first transaction associated with user's portfolio in cash profit.

        Args:
            owner_id (UUID): user's id.

        Returns:
            None
        """