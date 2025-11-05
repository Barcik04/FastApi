# src/user/PortfolioService.py
from uuid import UUID
from src.api.models.PortfolioOrm import PortfolioORM
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.db import SessionLocal


class PortfolioService:
    def __init__(self, repo: PortfolioRepository):
        self.repo = repo

    async def list_for_user(self, owner_id: UUID) -> list[PortfolioORM]:
        async with SessionLocal() as session:
            return await self.repo.list_for_user(session, owner_id)
