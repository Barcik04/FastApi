"""Dependency injection container for FastAPI services."""

from dependency_injector import containers, providers

from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TradeRequestRepository import TradeRequestRepository
from src.api.repositories.TransactionRepository import TransactionRepository
from src.api.repositories.UserRepository import UserRepository
from src.api.services.PortfolioService import PortfolioService
from src.api.services.TradeRequestService import TradeRequestService
from src.api.services.TransactionService import TransactionService
from src.api.services.UserService import UserService
from src.auth.AuthService import AuthService


class Container(containers.DeclarativeContainer):
    """Application container with service providers."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.routers.auth_router",
            "src.api.routers.portfolio_router",
            "src.api.routers.trade_request_router",
            "src.api.routers.transaction_router",
            "src.api.routers.user_router",
        ],
    )

    user_repository = providers.Factory(UserRepository)
    portfolio_repository = providers.Factory(PortfolioRepository)
    transaction_repository = providers.Factory(TransactionRepository)
    trade_request_repository = providers.Factory(TradeRequestRepository)

    user_service = providers.Factory(UserService, repo=user_repository)
    auth_service = providers.Factory(AuthService, repo=user_repository)
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

