"""Module containing TardeRequest repository implementation."""


from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select

from src.api.models.TradeRequestOrm import TradeRequestOrm


class TradeRequestRepository:
    """A class representing trade request DB repository."""


    async def show_user_requests(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        """The method getting all trade requests assigned to particular user.

            Args:
                owner_id (UUID): The id of user.
                session (AsyncSession): The database session.

            Returns:
                list[TradeRequestOrm]: Trade requests assigned to a user.
        """
        res = await session.execute(
            select(TradeRequestOrm).where((TradeRequestOrm.receiver_id==owner_id) | (TradeRequestOrm.sender_id==owner_id))
        )
        return res.scalars().all()




    async def show_user_senders(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        """The method getting all trade requests that were sent by user.

            Args:
                owner_id (UUID): The id of user.
                session (AsyncSession): The database session.

            Returns:
                list[TradeRequestOrm]: Trade requests assigned to a user if a trade is sent by this user.
        """
        res = await session.execute(
            select(TradeRequestOrm).where(TradeRequestOrm.sender_id==owner_id)
        )

        return res.scalars().all()




    async def show_user_receivers(self, session: AsyncSession, owner_id: UUID) -> list[TradeRequestOrm]:
        """The method getting all trade requests that were sent to user.

            Args:
                owner_id (UUID): The id of user.
                session (AsyncSession): The database session.

            Returns:
                list[TradeRequestOrm]: Trade requests assigned to a user if a trade is sent to this user.
        """
        res = await session.execute(
            select(TradeRequestOrm).where(TradeRequestOrm.receiver_id==owner_id)
        )

        return res.scalars().all()





    async def create_request(self, session: AsyncSession, coin: str, quantity: float, sender_id: UUID, receiver_id: UUID) -> TradeRequestOrm:
        """The method creating a trade request with given coin name, quantity, sender_id and receiver_id.

            Args:
                coin (str): The name of the coin.
                quantity (float): The quantity of the coin.
                sender_id (UUID): The id of the portfolio from where the coins are sent.
                receiver_id (UUID): The id of the portfolio from where the coins are received.
                session (AsyncSession): The database session.

            Returns:
                TradeRequestOrm: trade request object.
        """
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




    async def find_request(self, session: AsyncSession, request_id: UUID, receiver_id: UUID) -> TradeRequestOrm:
        """The method getting the request of given request_id if it also contains receiver_id.

            Args:
                request_id (UUID): The id of trade request.
                session (AsyncSession): The database session.
                receiver_id (UUID): The id of the portfolio from where the coins are received.

            Returns:
                TradeRequestOrm: Trade request found.
        """
        res = await session.execute(
            select(TradeRequestOrm).where((TradeRequestOrm.id==request_id) & (TradeRequestOrm.receiver_id==receiver_id))
        )
        return res.scalar()
