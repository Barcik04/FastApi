from datetime import datetime

from src.api.models.TransactionOrm import TransactionOrm
from src.api.repositories.TransactionRepository import TransactionRepository
from uuid import UUID

from src.db import SessionLocal


class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    async def show_user_transactions_between_date(self, start_date: datetime, end_date: datetime, owner_id: UUID) -> list[TransactionOrm]:
        async with SessionLocal() as session:
            async with session.begin():
                transactions = await self.repo.show_user_transactions_between_date(session, start_date, end_date, owner_id)

                return transactions