"""A module containing transaction endpoints."""

from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.infrastructure.services.ITransactionService import ITransactionService
from src.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.domain.Transaction import Transaction
from src.infrastructure.utils.deps import get_current_user_id
from src.container import Container


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[Transaction])
@inject
async def list_for_user(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITransactionService = Depends(Provide[Container.transaction_service]),
):
    """An endpoint for getting all transactions for the particular user.

    Args:
        user_id (UUID): The authenticated user ID fetched from JWT.
        service (ITransactionService, optional): The injected service dependency.
        session (AsyncSession): The injected session dependency.

    Returns:
        list[Transaction]: The list of user transactions.
    """
    return await service.list_for_user(user_id, session)



@router.get("/val")
@inject
async def graph_portfolio_val(
    days: int,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITransactionService = Depends(Provide[Container.transaction_service]),
):
    """An endpoint for generating portfolio value graph with given days.

      Args:
          days (int): The number of days to display the graph in the past.
          user_id (UUID): The authenticated user ID fetched from the JWT.
          service (ITransactionService, optional): The injected service dependency.
          session (AsyncSession): The injected session dependency.

      Returns:
          None: Displays a graph window on the server side.
      """
    return await service.graph_portfolio_val(user_id, days, session)


@router.get("/sep-coins")
@inject
async def graph_multiple_coins(
    days: int,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITransactionService = Depends(Provide[Container.transaction_service]),
):
    """An endpoint for generating graph showing each coin PnL separately.

        Args:
            days (int): The number of days in the past to include in the calculation.
            user_id (UUID): The authenticated user ID fetched from the JWT.
            service (ITransactionService, optional): The injected service dependency.
            session (AsyncSession): The injected session dependency.

        Returns:
            None: Displays graph.
        """
    return await service.graph_multiple_coins(user_id, days, session)


@router.get("/p_n_l_perc", response_model=None)
@inject
async def graph_p_n_l_percent(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITransactionService = Depends(Provide[Container.transaction_service]),
):
    """An endpoint for generating percentage-based PnL graph.

       Args:
           user_id (UUID): The authenticated user ID fetched from the JWT.
           service (ITransactionService, optional): The injected service dependency.
           session (AsyncSession): The injected session dependency.

       Returns:
           None: Displays a graph showing profit and loss in percentages.
       """
    return await service.graph_p_n_l_percent(user_id, session)


@router.get("/p_n_l")
@inject
async def graph_p_n_l(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
    service: ITransactionService = Depends(Provide[Container.transaction_service]),
):
    """An endpoint for generating graph of PnL profit and loss in coin value.

    Args:
        user_id (UUID): The authenticated user ID fetched from the JWT.
        service (ITransactionService, optional): The injected service dependency.
        session (AsyncSession): The injected session dependency.

    Returns:
        None: Displays a graph with PnL profit and loss in coin value.
    """
    return await service.graph_p_n_l(user_id, session)