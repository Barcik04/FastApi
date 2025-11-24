"""A module containing trade request endpoints."""


from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.IPortfolioService import IPortfolioService
from src.db import get_session

from src.api.schemas.Portfolio import Portfolio
from src.auth.utils.deps import get_current_user_id
from src.container import Container

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=Portfolio)
@inject
async def show_user_portfolio(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for getting the authenticated user's portfolio.

       Args:
           user_id (UUID): The authenticated user ID fetched from the JWT token.
           service (IPortfolioService, optional): The injected service dependency.
           session (AsyncSession): the injected DB session.

       Returns:
           Portfolio: The portfolio of the user.
       """
    return await service.show_user_portfolio(user_id, session)


@router.post("/buy", response_class=PlainTextResponse)
@inject
async def buy_crypto(
    coin: str,
    quantity: float,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for buying crypto.

       Args:
           coin (str): name of the crypto to buy.
           quantity (float): The quantity of the crypto to buy.
           user_id (UUID): The authenticated user ID fetched from the JWT token.
           service (IPortfolioService, optional): The injected service dependency.
           session (AsyncSession): the injected DB session.

       Returns:
           str: A confirmation message.
       """
    return await service.buy_crypto(user_id, coin, quantity, session)


@router.post("/sell", response_class=PlainTextResponse)
@inject
async def sell_crypto(
    coin: str,
    quantity: str,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for selling crypto.

       Args:
           coin (str): the name of the crypto to sell.
           quantity (str): The quantity of the crypto to sell.
           user_id (UUID): The authenticated user ID fetched from the JWT token.
           service (IPortfolioService, optional): The injected service dependency.
           session (AsyncSession): The injected DB session.

       Returns:
           str: A confirmation message.
       """
    return await service.sell_crypto(user_id, coin, quantity, session)




@router.post("/deposit", response_class=PlainTextResponse)
@inject
async def deposit_tether(
    quantity: float,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for depositing tether.

        Args:
            quantity (float): The amount of tether to deposit.
            user_id (UUID): The authenticated user ID fetched from the JWT token.
            service (IPortfolioService, optional): The injected service dependency.
            session (AsyncSession): the injected DB session.

        Returns:
            str: A confirmation message.
        """
    return await service.deposit_tether(user_id, quantity, session)




@router.post("/withdraw", response_class=PlainTextResponse)
@inject
async def withdraw_tether(
    quantity: str,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for withdrawing tether.

      Args:
          quantity (str): The amount of Tether to withdraw.
          user_id (UUID): The authenticated user ID fetched from the JWT token.
          service (IPortfolioService, optional): The injected service dependency.
          session (AsyncSession): The injected DB session.

      Returns:
          str: A confirmation message.
      """
    return await service.withdraw_tether(user_id, quantity, session)


@router.get("/p_and_l_coin", response_model=dict)
@inject
async def profit_and_loss_for_coin(
    coin: str,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for displaying profit and losses for the given coin.

       Args:
           coin (str): The name of the crypto to show graph for.
           user_id (UUID): The authenticated user ID fetched from the JWT token.
           service (IPortfolioService, optional): The injected service dependency.
           session (AsyncSession): the injected DB session.

       Returns:
           dict: The profit and loss details for the given coin.
       """
    return await service.p_and_l_coin(user_id, coin, session)


@router.post("/transfer", response_class=PlainTextResponse)
@inject
async def transfer_coin(
    coin: str,
    quantity: str,
    transfer_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: IPortfolioService = Depends(Provide[Container.portfolio_service]),
):
    """An endpoint for transferring crypto between users.

       Args:
           coin (str): The name of the crypto to transfer.
           quantity (str): The quantity of the crypto to transfer.
           transfer_id (UUID): The ID of the user's portfolio receiving the transfer.
           user_id (UUID): The authenticated user ID fetched from the JWT token.
           service (IPortfolioService, optional): The injected service dependency.
           session (AsyncSession): the injected DB session.

       Returns:
           str: A confirmation message.
       """
    return await service.transfer_coin(user_id, coin, quantity, transfer_id, session)


