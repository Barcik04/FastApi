"""Module containing trade request service abstractions."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.api.models.TradeRequestOrm import TradeRequestOrm
from src.api.schemas.TradeRequest import TradeRequestIn


class ITradeRequestService(ABC):
    """An abstract base class representing a trade request service."""

    @abstractmethod
    async def show_user_requests(self, owner_id: UUID) -> list[TradeRequestOrm]:
        """Get trade requests for user.

        Args:
            owner_id (UUID): The id of the user.

        Returns:
            list[TradeRequestOrm]: Trade requests assigned to the user.
        """

    @abstractmethod
    async def create_user_request(self, body: TradeRequestIn, owner_id: UUID) -> str:
        """Create a trade request with specified coin and quantity and portfolio_id we want to make a trade with.

        Args:
            body (TradeRequestIn): DTO containing coin, quantity, and receiver id.
            owner_id (UUID): The id of the user creating the request.

        Returns:
            str: Information about the transaction status.
        """

    @abstractmethod
    async def update_user_request(self, owner_id: UUID, accept: bool, request_id: UUID) -> str:
        """accept or reject a trade request and proceed money transaction automatically.

        Args:
            owner_id (UUID): The id of the user.
            accept (bool): Whether to accept the trade request.
            request_id (UUID): The id of the trade request.

        Returns:
            str: Information about the transaction status.
        """