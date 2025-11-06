# src/user/PortfolioService.py
from uuid import UUID

import httpx
from fastapi import HTTPException

from src.api.models.PortfolioOrm import PortfolioORM
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.db import SessionLocal


class PortfolioService:
    def __init__(self, repo: PortfolioRepository):
        self.repo = repo

    async def show_user_portfolio(self, owner_id: UUID) -> PortfolioORM:
        async with SessionLocal() as session:
            return await self.repo.show_user_portfolio(session, owner_id)

    async def buy_crypto(self, owner_id: UUID, coin: str, quantity: float) -> PortfolioORM:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                prev_quantity = portfolio.coins.get(coin, 0.0)
                prev_avg_price = portfolio.bought_price.get(coin, 0.0)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": coin, "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()[coin]["usd"]



                if prev_quantity == 0:
                    coins = dict(portfolio.coins)
                    coins[coin] = coins.get(coin, 0) + quantity
                    portfolio.coins = coins

                    new_avg_price = (((prev_avg_price / 1) * prev_quantity) + (price_usd * quantity)) / (prev_quantity + quantity)

                    bought_price = dict(portfolio.bought_price)
                    bought_price[coin] = new_avg_price
                    portfolio.bought_price = bought_price

                    return portfolio


                new_avg_price = (prev_avg_price * prev_quantity + price_usd * quantity) / (prev_quantity + quantity)
                # ((101/1) * 1) + ((101/1) * 1)) / 1 + 1 = (101 + 101) / 2
                # (101 * 2 + 101 * 1) / 3 = 101
                # (101 * 3 + 101 * 1) /

                coins = dict(portfolio.coins)
                coins[coin] = coins.get(coin, 0) + quantity
                portfolio.coins = coins

                bought_price = dict(portfolio.bought_price)
                bought_price[coin] = new_avg_price
                portfolio.bought_price = bought_price

                return portfolio


    async def sell_crypto(self, owner_id: UUID, coin: str, quantity: float) -> PortfolioORM:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)
                quantity_portfolio = portfolio.coins.get(coin, 0.0)

                if quantity_portfolio < quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough {coin} to sell. You have {coins.get(coin)}.")


                if coin not in coins:
                    raise HTTPException(status_code=404, detail=f"No '{coin}' in your portfolio.")


                coins[coin] = coins.get(coin) - quantity
                if coins[coin] == 0:
                    coins.pop(coin)
                    bought_price.pop(coin)





                portfolio.coins = coins
                portfolio.bought_price = bought_price



                return portfolio

