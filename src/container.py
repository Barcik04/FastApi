
from dependency_injector import containers, providers

from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TradeRequestRepository import TradeRequestRepository
from src.api.repositories.TransactionRepository import TransactionRepository
from src.api.repositories.UserRepository import UserRepository
from src.api.services.PortfolioService import PortfolioService
from src.api.services.TradeRequestService import TradeRequestService
from src.api.services.TransactionService import TransactionService
from src.api.services.UserService import UserService


class Container(containers.DeclarativeContainer):

    user_repository = providers.Singleton(UserRepository)
    portfolio_repository = providers.Singleton(PortfolioRepository)
    transaction_repository = providers.Singleton(TransactionRepository)
    trade_request_repository = providers.Singleton(TradeRequestRepository)

    user_service = providers.Factory(UserService, repo=user_repository)

    portfolio_service = providers.Factory(
        PortfolioService,
        repo=portfolio_repository,
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repo=transaction_repository,
        portfolio_repo=portfolio_repository,
    )

    trade_request_service = providers.Factory(
        TradeRequestService,
        trade_request_repo=trade_request_repository,
        portfolio_repo=portfolio_repository,
    )
