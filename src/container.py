from dependency_injector import containers, providers

from src.infrastructure.repositories.PortfolioRepository import PortfolioRepository
from src.infrastructure.repositories.TradeRequestRepository import (
    TradeRequestRepository,
)
from src.infrastructure.repositories.TransactionRepository import TransactionRepository
from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.services.PortfolioService import PortfolioService
from src.infrastructure.services.TradeRequestService import TradeRequestService
from src.infrastructure.services.TransactionService import TransactionService
from src.infrastructure.services.UserService import UserService
from src.infrastructure.services.MessageService import MessageService
from src.infrastructure.repositories.MessageRepository import MessageRepository


class Container(containers.DeclarativeContainer):

    user_repository = providers.Singleton(UserRepository)
    portfolio_repository = providers.Singleton(PortfolioRepository)
    transaction_repository = providers.Singleton(TransactionRepository)
    trade_request_repository = providers.Singleton(TradeRequestRepository)
    message_repository = providers.Singleton(MessageRepository)

    user_service = providers.Factory(UserService, repository=user_repository)

    portfolio_service = providers.Factory(
        PortfolioService,
        repository=portfolio_repository,
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repository=transaction_repository,
        portfolio_repository=portfolio_repository,
    )

    trade_request_service = providers.Factory(
        TradeRequestService,
        trade_request_repository=trade_request_repository,
        portfolio_repository=portfolio_repository,
    )

    message_service = providers.Factory(
        MessageService,
        repository=message_repository,
    )
