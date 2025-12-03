
from dependency_injector import containers, providers

from src.infrastructure.repositories.PortfolioRepository import PortfolioRepository
from src.infrastructure.repositories.TradeRequestRepository import TradeRequestRepository
from src.infrastructure.repositories.TransactionRepository import TransactionRepository
from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.services import PortfolioService
from src.infrastructure.services import TradeRequestService
from src.infrastructure.services.TransactionService import TransactionService
from src.infrastructure.services.UserService import UserService


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
