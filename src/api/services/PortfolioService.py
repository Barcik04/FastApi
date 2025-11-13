# src/user/PortfolioService.py
from datetime import datetime
from uuid import UUID

import httpx
from fastapi import HTTPException

from src.api.models.TransactionOrm import TransactionOrm
from src.api.models.PortfolioOrm import PortfolioORM
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.db import SessionLocal


class PortfolioService:
    def __init__(self, repo: PortfolioRepository):
        self.repo = repo

    async def show_user_portfolio(self, owner_id: UUID) -> PortfolioORM:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)
                p_and_l = 0.0
                account_val = 0.0

                for coin in coins:
                    url = "https://api.coingecko.com/api/v3/simple/price"
                    params = {"ids": coin, "vs_currencies": "usd"}

                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params)
                        response.raise_for_status()
                        price_usd = response.json()[coin]["usd"]

                    coin_bought_price = bought_price[coin] #101
                    price_diff = price_usd / coin_bought_price #107 / 101 = 1.059

                    coin_val = coins[coin] * price_usd * price_diff # 21 * 107 * 1.059 = 2379
                    p_and_l += coin_val - (coins[coin] * price_usd) # 2379 - (21 * 107) = 132
                    account_val += price_usd * coins.get(coin)

                portfolio.p_and_l = p_and_l


                return portfolio



    async def buy_crypto(self, owner_id: UUID, coin: str, quantity: float) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)

                prev_quantity = portfolio.coins.get(coin, 0.0)
                prev_avg_price = portfolio.bought_price.get(coin, 0.0)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": coin, "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()[coin]["usd"]

                coin_value = price_usd * quantity # 102 000
                tether = coins.get("tether", 0.0) #900 000


                if coin_value > tether:
                    raise HTTPException(status_code=400, detail=f"Not enough theater in your account to buy: {quantity} of {coin}.")

                coins["tether"] = coins.get("tether") - coin_value  # tether = 900 000 - 102 000

                if prev_quantity == 0:
                    coins[coin] = coins.get(coin, 0) + quantity
                    portfolio.coins = coins


                    new_avg_price = (((prev_avg_price / 1) * prev_quantity) + (price_usd * quantity)) / (prev_quantity + quantity)

                    bought_price[coin] = new_avg_price
                    portfolio.bought_price = bought_price

                    tr = TransactionOrm(
                        owner_id=owner_id,
                        coin=coin,
                        date=datetime.now(),
                        quantity=quantity,
                        bought_price=price_usd
                    )
                    session.add(tr)

                    return f"Transaction successful! Bought: {quantity}, of {coin}, with price: {price_usd}"



                new_avg_price = (prev_avg_price * prev_quantity + price_usd * quantity) / (prev_quantity + quantity)
                # ((101/1) * 1) + ((101/1) * 1)) / 1 + 1 = (101 + 101) / 2
                # (101 * 2 + 101 * 1) / 3 = 101
                # (101 * 3 + 101 * 1) /

                coins[coin] = coins.get(coin, 0) + quantity
                portfolio.coins = coins

                bought_price[coin] = new_avg_price
                portfolio.bought_price = bought_price

                tr = TransactionOrm(
                    owner_id=owner_id,
                    coin=coin,
                    date=datetime.now(),
                    quantity=quantity,
                    bought_price=price_usd
                )
                session.add(tr)

                return f"Transaction successful! Bought: {quantity}, of {coin}, with price: {price_usd}"



    async def sell_crypto(self, owner_id: UUID, coin: str, quantity: str) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)
                quantity_portfolio = portfolio.coins.get(coin, 0.0)

                if quantity == "all":
                    quantity = coins.get(coin, 0.0)
                else:
                    quantity = float(quantity)

                if quantity_portfolio < quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough {coin} to sell. You have {coins.get(coin)}.")


                if coin not in coins:
                    raise HTTPException(status_code=404, detail=f"No '{coin}' in your portfolio.")


                coins[coin] = coins.get(coin) - quantity
                if coins[coin] == 0:
                    coins.pop(coin)
                    bought_price.pop(coin)


                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": coin, "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()[coin]["usd"]

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": "tether", "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    tether_price = response.json()["tether"]["usd"]


                coins.get("tether", 0.0)
                tether = bought_price.get("tether", tether_price)
                coins["tether"] += quantity * price_usd
                bought_price["tether"] = tether

                portfolio.coins = coins
                portfolio.bought_price = bought_price

                tr = TransactionOrm(
                    owner_id=owner_id,
                    coin=coin,
                    date=datetime.now(),
                    quantity=quantity * (-1)
                )
                session.add(tr)

                return f"Transaction successful! Sold: {quantity}, of {coin}, with price: {price_usd}"


    async def deposit_tether(self, owner_id: UUID, quantity: float) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                bought_price = dict(portfolio.bought_price)
                coins = dict(portfolio.coins)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": "tether", "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["tether"]["usd"]

                tether = coins.get("tether", 0.0)

                coins["tether"] = tether + quantity
                bought_price["tether"] = bought_price.get("tether", price_usd)

                portfolio.coins = coins
                portfolio.bought_price = bought_price

                return f"Transaction successful! {quantity} of theater bought!"


    async def withdraw_tether(self, owner_id: UUID, quantity: str) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                if portfolio is None:
                    raise HTTPException(status_code=404, detail="Portfolio not found for this user.")

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": "tether", "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["tether"]["usd"]


                if quantity == "all":
                    quantity = coins.get("tether", 0.0)
                else:
                    quantity = float(quantity)


                if coins.get("tether", 0.0) < quantity:
                    raise HTTPException(status_code=404, detail=f"Not enough tether in your portfolio.")

                coins["tether"] = coins.get("tether", 0.0) - quantity
                usd = (2 - price_usd) * quantity



                if coins.get("tether") == 0:
                    bought_price.pop("tether")

                portfolio.coins = coins
                portfolio.bought_price = bought_price

                return f"Withdrawal successful! You withdrew: {quantity} of tether. {usd} USD will be transferred into your bank account shortly"


    async def p_and_l_coin(self, owner_id: UUID, coin: str) -> dict[str, float]:
        async with SessionLocal() as session:
            async with session.begin():
                portfolio = await self.repo.show_user_portfolio(session, owner_id)

                coins = dict(portfolio.coins)
                bought_price = dict(portfolio.bought_price)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": coin, "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()[coin]["usd"]

                if coin not in coins:
                    raise HTTPException(status_code=400, detail=f"{coin} not in your portfolio.")

                bought_val = bought_price.get(coin)
                coin_quant = coins.get(coin)

                p_and_l_percent = (1 - price_usd / bought_val) * 100
                p_and_l = (price_usd * coin_quant) - (bought_val * coin_quant)

                results =  {
                    "p_and_l": p_and_l,
                    "p_and_l_percent": p_and_l_percent
                }

                return results


    async def transfer_coin(self, owner_id: UUID, coin: str, quantity: str, transfer_id: UUID) -> str:
        async with SessionLocal() as session:
            async with session.begin():
                my_portfolio = await self.repo.show_user_portfolio(session, owner_id)
                target_portfolio = await self.repo.show_user_portfolio(session, transfer_id)
                target_portfolio = target_portfolio.id

                my_coins = dict(my_portfolio.coins)

                target_coins = dict(target_portfolio.coins)
                target_bought_price = dict(target_portfolio.bought_price)



                if coin not in my_coins:
                    raise HTTPException(status_code=400, detail=f"{coin} not found in your portfolio.")

                if quantity == "all":
                    quantity = my_coins.get(coin, 0.0)
                else:
                    quantity = float(quantity)

                if my_coins[coin] < quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough {coin} in your portfolio.")


                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": coin, "vs_currencies": "usd"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()[coin]["usd"]


                my_coins[coin] -= quantity
                target_coins[coin] = target_coins.get(coin, 0.0) + quantity
                target_bought_price.setdefault(coin, price_usd)

                if my_coins.get(coin) == 0:
                    my_coins.pop(coin)
                    target_bought_price.pop(coin)

                my_portfolio.coins = my_coins
                target_portfolio.coins = target_coins
                ### this will overwrite bought_price, and it should calculate new avg_bought_price
                target_portfolio.bought_price = target_bought_price


                return f"Transaction successful! {quantity} of {coin} transferred to portfolio with id: {target_portfolio} ."
