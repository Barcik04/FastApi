import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from uuid import UUID

from fastapi import HTTPException

from src.api.models.CryptoDataOrm import CryptoDataOrm
from src.db import SessionLocal
from src.api.repositories.CryptoDataRepository import CryptoDataRepository


class CryptoDataService:
    def __init__(self, repo: CryptoDataRepository | None = None):
        self.repo = repo or CryptoDataRepository()

    async def list_for_user(self, owner_id: UUID) -> list[CryptoDataOrm]:
        async with SessionLocal() as session:
            async with session.begin():
                return await self.repo.show_user_data(session, owner_id)


    async def list_of_amount_for_user(self, owner_id: UUID, mode: int) -> None:
        async with SessionLocal() as session:
            async with session.begin():
                crypto_data = await self.repo.show_user_data(session, owner_id)

                dates = []
                amounts = []

                if mode == 1:
                    for crypto in crypto_data:
                        amounts.append(crypto.amount)
                        dates.append(crypto.date)

                elif mode == 2:
                    for crypto in crypto_data:
                        amounts.append(crypto.amount_p_and_l)  # P/L column
                        dates.append(crypto.date)

                else:
                    raise HTTPException(status_code=400, detail="Invalid mode. Use 1 or 2.")

                plt.plot(dates, amounts)
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.gcf().autofmt_xdate()
                plt.xlabel("Date")
                plt.ylabel("Amount")
                plt.title("Amount Over Time" if mode == 1 else "Profit & Loss Over Time")
                plt.tight_layout()
                plt.show()