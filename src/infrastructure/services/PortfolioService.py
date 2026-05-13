"""Module containing portfolio service implementation."""

from typing import Iterable
from datetime import datetime
from uuid import UUID

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models.TransactionOrm import TransactionOrm
from src.infrastructure.models.PortfolioOrm import PortfolioOrm
from src.core.irepositories.iportfolio import IPortfolioRepository
from src.infrastructure.services.IPortfolioService import IPortfolioService


class PortfolioService(IPortfolioService):
    """A class implementing the portfolio service."""

    _repository: IPortfolioRepository

    def __init__(self, repository: IPortfolioRepository) -> None:
        """The initializer of the `portfolio service`.

        Args:
            repository (IPortfolioRepository): The reference to the repository.
        """
        self._repository = repository

    async def show_user_portfolio(
        self, owner_id: UUID, session: AsyncSession
    ) -> PortfolioOrm:
        """The method getting portfolio assigned to particular user.

        Args:
            owner_id (UUID): The id of the user.
            session (AsyncSession): DB session.

        Returns:
            PortfolioOrm: portfolio assigned to a user.
        """

        if session is None:
            raise ValueError("session cannot be None")

        if owner_id is None:
            raise ValueError("owner_id cannot be None")

        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            if portfolio is None:
                raise ValueError("user has no portfolio")


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

                if coin not in bought_price:
                    raise ValueError(f"missing bought price for coin: {coin}")

                coin_bought_price = bought_price[coin]
                price_diff = price_usd / coin_bought_price

                coin_val = coins[coin] * price_usd * price_diff
                p_and_l += coin_val - (coins[coin] * price_usd)
                account_val += price_usd * coins.get(coin)

            portfolio.p_and_l = p_and_l
            return portfolio



    async def buy_crypto(
        self, owner_id: UUID, coin: str, quantity: float, session: AsyncSession
    ) -> str:
        """The method proceeds to assign coin with given quantity to user portfolio
        plus creates transaction object and insert it into transaction table.

        Args:
            owner_id (UUID): The id of the user.
            coin (str): name of the coin to buy.
            quantity (float): quantity of the coin to buy.
            session (AsyncSession): DB session.

        Returns:
            str: message with transaction information.
        """

        if session is None:
            raise ValueError("session cannot be None")

        if owner_id is None:
            raise ValueError("owner_id cannot be None")

        if coin is None:
            raise ValueError("coin cannot be None")

        if coin == "":
            raise ValueError("coin cannot be empty")

        if quantity is None:
            raise ValueError("quantity cannot be None")

        if quantity <= 0:
            raise ValueError("quantity cannot be 0 or lower")

        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            if portfolio is None:
                raise ValueError("user has no portfolio")

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

            coin_value = price_usd * quantity
            tether = coins.get("tether", 0.0)

            if coin_value > tether:
                raise ValueError(f"Not enough theater in your account to buy: {quantity} of {coin}.")

            coins["tether"] = coins.get("tether") - coin_value

            if prev_quantity == 0:
                coins[coin] = coins.get(coin, 0) + quantity
                portfolio.coins = coins

                new_avg_price = (
                    ((prev_avg_price / 1) * prev_quantity) + (price_usd * quantity)
                ) / (prev_quantity + quantity)

                bought_price[coin] = new_avg_price
                portfolio.bought_price = bought_price

                tr = TransactionOrm(
                    owner_id=owner_id,
                    coin=coin,
                    date=datetime.now(),
                    quantity=quantity,
                    bought_price=price_usd,
                )
                session.add(tr)

                return f"Transaction successful! Bought: {quantity}, of {coin}, with price: {price_usd}"

            new_avg_price = (prev_avg_price * prev_quantity + price_usd * quantity) / (
                prev_quantity + quantity
            )

            coins[coin] = coins.get(coin, 0) + quantity
            portfolio.coins = coins

            bought_price[coin] = new_avg_price
            portfolio.bought_price = bought_price

            tr = TransactionOrm(
                owner_id=owner_id,
                coin=coin,
                date=datetime.now(),
                quantity=quantity,
                bought_price=price_usd,
            )
            session.add(tr)

            return f"Transaction successful! Bought: {quantity}, of {coin}, with price: {price_usd}"


    async def sell_crypto(
        self, owner_id: UUID, coin: str, quantity: str, session: AsyncSession
    ) -> str:
        """The method updates user portfolio and sells given coin and its quantity
        if theres enough coin in user portfolio

        Args:
            owner_id (UUID): The id of the user.
            coin (str): name of the coin to buy.
            quantity (str): quantity of the coin to buy ("all" or number).
            session (AsyncSession): DB session.

        Returns:
            str: message with transaction information.
        """

        if session is None:
            raise ValueError("session cannot be None")

        if owner_id is None:
            raise ValueError("owner_id cannot be None")

        if coin is None:
            raise ValueError("coin cannot be None")

        if coin == "":
            raise ValueError("coin cannot be empty")

        if quantity is None:
            raise ValueError("quantity cannot be None")

        if quantity <= 0:
            raise ValueError("quantity cannot be 0 or lower")


        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            if portfolio is None:
                raise ValueError("user has no portfolio")

            coins = dict(portfolio.coins)
            bought_price = dict(portfolio.bought_price)
            quantity_portfolio = portfolio.coins.get(coin, 0.0)

            if quantity == "all":
                quantity = coins.get(coin, 0.0)
            else:
                quantity = float(quantity)

            if coin not in coins:
                raise ValueError(f"No '{coin}' in your portfolio.")

            if quantity_portfolio < quantity:
                raise ValueError(f"Not enough coin in your account to sell: {quantity} of {coin}.")



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

            coins["tether"] = coins.get("tether", 0.0) + quantity * price_usd
            bought_price["tether"] = bought_price.get("tether", tether_price)

            portfolio.coins = coins
            portfolio.bought_price = bought_price

            tr = TransactionOrm(
                owner_id=owner_id,
                coin=coin,
                date=datetime.now(),
                quantity=quantity * (-1),
            )
            session.add(tr)

            return f"Transaction successful! Sold: {quantity}, of {coin}, with price: {price_usd}"

    async def deposit_tether(
        self, owner_id: UUID, quantity: float, session: AsyncSession
    ) -> str:
        """The method updates user portfolio and adds "tether" coin which is used to buy other coins.

        Args:
            owner_id (UUID): The id of the user.
            quantity (float): quantity of tether to buy.
            session (AsyncSession): DB session.

        Returns:
            str: message with transaction information.
        """

        if session is None:
            raise ValueError("session cannot be None")

        if owner_id is None:
            raise ValueError("owner_id cannot be None")

        if quantity is None:
            raise ValueError("quantity cannot be None")

        if quantity <= 0:
            raise ValueError("quantity cannot be 0 or lower")

        if quantity > 1_000_000_000:
            raise ValueError("quantity is too large")

        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            if portfolio is None:
                raise ValueError("user has no portfolio")

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

    async def withdraw_tether(
        self, owner_id: UUID, quantity: str, session: AsyncSession
    ) -> str:
        """The method proceeds to withdraw tether from user portfolio to user's "bank account".

        Args:
            owner_id (UUID): The id of the user.
            quantity (str): quantity of the tether to withdraw ("all" or number).
            session (AsyncSession): DB session.

        Returns:
            str: message with transaction information.
        """


        if session is None:
            raise ValueError("session cannot be None")

        if owner_id is None:
            raise ValueError("owner_id cannot be None")

        if quantity is None:
            raise ValueError("quantity cannot be None")

        if quantity <= 0:
            raise ValueError("quantity cannot be 0 or lower")

        if quantity > 1_000_000_000:
            raise ValueError("quantity is too large")


        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            if portfolio is None:
                raise ValueError("user has no portfolio")

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
                raise ValueError("Not enough tether in your portfolio.")

            coins["tether"] = coins.get("tether", 0.0) - quantity
            usd = (2 - price_usd) * quantity

            if coins.get("tether") == 0:
                bought_price.pop("tether")
                coins.pop("tether")

            portfolio.coins = coins
            portfolio.bought_price = bought_price

            return (
                f"Withdrawal successful! You withdrew: {quantity} of tether. "
                f"{usd} USD will be transferred into your bank account shortly"
            )

    async def p_and_l_coin(
        self, owner_id: UUID, coin: str, session: AsyncSession
    ) -> dict[str, float]:
        """method calculates and displays profit and losses for the given coin.

        Args:
            owner_id (UUID): The id of the user.
            coin (str): name of the coin to calculate profit and losses.
            session (AsyncSession): DB session.

        Returns:
            dict[str, float]: dictionary with p_n_L in $ and %.
        """

        async with session.begin():
            portfolio = await self._repository.show_user_portfolio(session, owner_id)

            coins = dict(portfolio.coins)
            bought_price = dict(portfolio.bought_price)

            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {"ids": coin, "vs_currencies": "usd"}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                price_usd = response.json()[coin]["usd"]

            if coin not in coins:
                raise HTTPException(
                    status_code=400, detail=f"{coin} not in your portfolio."
                )

            bought_val = bought_price.get(coin)
            coin_quant = coins.get(coin)

            p_and_l_percent = (1 - price_usd / bought_val) * 100
            p_and_l = (price_usd * coin_quant) - (bought_val * coin_quant)

            return {"p_and_l": p_and_l, "p_and_l_percent": p_and_l_percent}

    async def transfer_coin(
        self,
        owner_id: UUID,
        coin: str,
        quantity: str,
        transfer_id: UUID,
        session: AsyncSession,
    ) -> str:
        """method transfers coin with given quantity to portfolio with transfer_id.

        Args:
            owner_id (UUID): The id of the user.
            coin (str): name of the coin to transfer.
            quantity (str): quantity to transfer ("all" or number).
            transfer_id (UUID): transfer id of portfolio to transfer to.
            session (AsyncSession): DB session.

        Returns:
            str: basic status information of the transfer.
        """

        async with session.begin():
            my_portfolio = await self._repository.show_user_portfolio(session, owner_id)
            target_portfolio = await self._repository.find_portfolio_by_id(
                session, transfer_id
            )

            my_coins = dict(my_portfolio.coins)
            target_coins = dict(target_portfolio.coins)
            target_bought_price = dict(target_portfolio.bought_price)

            if coin not in my_coins:
                raise HTTPException(
                    status_code=400, detail=f"{coin} not found in your portfolio."
                )

            if quantity == "all":
                quantity = my_coins.get(coin, 0.0)
            else:
                quantity = float(quantity)

            if my_coins[coin] < quantity:
                raise HTTPException(
                    status_code=400, detail=f"Not enough {coin} in your portfolio."
                )

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
            target_portfolio.bought_price = target_bought_price

            return f"Transaction successful! {quantity} of {coin} transferred to portfolio with id: {target_portfolio} ."
