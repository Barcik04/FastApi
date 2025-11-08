from uuid import UUID
from src.db import SessionLocal
from src.api.repositories.CryptoDataRepository import CryptoDataRepository


class CryptoDataService:
    def __init__(self, repo: CryptoDataRepository | None = None):
        self.repo = repo or CryptoDataRepository()

    async def list_for_user(self, owner_id: UUID):
        async with SessionLocal() as session:
            async with session.begin():
                return await self.repo.show_user_data(session, owner_id)

