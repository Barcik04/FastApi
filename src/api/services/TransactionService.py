"""Module containing transaction service implementation."""

from datetime import datetime, timedelta, timezone

import httpx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from uuid import UUID
import numpy as np
from fastapi import HTTPException
import io
from fastapi.responses import StreamingResponse

from src.api.models.TransactionOrm import TransactionOrm
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TransactionRepository import TransactionRepository
from src.api.services.ITransactionService import ITransactionService
from sqlalchemy.ext.asyncio import AsyncSession



class TransactionService(ITransactionService):
    """A class implementing the transaction service."""
    def __init__(
            self,
            transaction_repo: TransactionRepository | None = None,
            portfolio_repo: PortfolioRepository | None = None,
    ):
        self.transaction_repo = transaction_repo or TransactionRepository()
        self.portfolio_repo = portfolio_repo or PortfolioRepository()


    async def list_for_user(self, owner_id: UUID, session: AsyncSession) -> list[TransactionOrm]:
        """The method for getting transactions made by a particular user.

            Args:
                owner_id (int): The id of the user.
                session (AsyncSession): The database session.

            Returns:
                list[TransactionOrm]: list of transactions assigned to particular user
        """

        async with session.begin():
            return await self.transaction_repo.show_user_transactions(session, owner_id)




    async def graph_portfolio_val(self, owner_id: UUID, days: int, session: AsyncSession) -> None:
        """The method for generating a graph showing the portfolio value up to a year backwards.

            Args:
                owner_id (int): The id of the user.
                days (int): number of days backwards to track value of portfolio
                session (AsyncSession): DB session

            Returns:
                None
        """

        async with session.begin():
            if days <= 0:
                raise HTTPException(status_code=403, detail="Number of days cant be 0 or less")

            now = datetime.now(timezone.utc)
            portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)

            total_portfolio_val = [0] * 284

            days_back = int(days)

            for crypto in portfolio.coins:
                if crypto == "tether":
                    continue
                transactions = await self.transaction_repo.show_user_transactions_between_date_by_coin(session, now - timedelta(days=days_back), now, owner_id, crypto)
                portfolio_quant = portfolio.coins.get(crypto, 0.0)

                quants = []
                for tx in transactions:
                    quants.append(tx.quantity)
                portfolio_transactions_quant = 0
                for q in quants:
                    portfolio_transactions_quant += q # 0.5
                portfolio_start_quant = portfolio_quant - portfolio_transactions_quant # 0.2

                url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
                params = {"vs_currency": "usd", "days": f"{days_back}"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["prices"]

                sorted_transactions = sorted(transactions, key=lambda x: x.date)


                prices = []
                timestamps = []
                for timestamp, price in price_usd:
                    time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                    prices.append(price * portfolio_start_quant)
                    timestamps.append(time)



                prices_usd = []
                for price in price_usd:
                    prices_usd.append(price[1])

                prices_final = []
                previous_timestamp = timestamps[0]

                for timestamp, price in zip(timestamps, prices_usd):
                    if not sorted_transactions:
                        prices_final.append(price * portfolio_start_quant)
                        previous_timestamp = timestamp
                        continue

                    if timestamp == timestamps[0]:
                        if sorted_transactions[0].date <= timestamp:
                            prices_final.append(price * (portfolio_start_quant + sorted_transactions[0].quantity))
                            sorted_transactions.remove(sorted_transactions[0])
                            portfolio_start_quant += sorted_transactions[0].quantity
                            previous_timestamp = timestamp
                        else:
                            prices_final.append(price * portfolio_start_quant)
                            previous_timestamp = timestamp
                        continue
                    elif timestamp > sorted_transactions[0].date > previous_timestamp:
                        prices_final.append(price * (portfolio_start_quant + sorted_transactions[0].quantity))
                        portfolio_start_quant += sorted_transactions[0].quantity
                        sorted_transactions.remove(sorted_transactions[0])
                        previous_timestamp = timestamp
                        continue
                    else:
                        prices_final.append(price * portfolio_start_quant)
                        previous_timestamp = timestamp

                for i in range(len(prices_final)):
                    if i >= len(total_portfolio_val):
                        break
                    total_portfolio_val[i] += prices_final[i]


            if len(timestamps) <= len(total_portfolio_val):
                total_portfolio_val = total_portfolio_val[:len(timestamps)]


            if len(timestamps) > len(total_portfolio_val):
                timestamps = timestamps[:len(total_portfolio_val)]


            filter_ts = []
            filtered_vals = []


            for i in range(len(total_portfolio_val) - 1):
                if timestamps[i] > sorted_transactions[0].date:
                    filter_ts.append(timestamps[i])
                    filtered_vals.append(total_portfolio_val[i])


            legend = {k: round(v, 3) for k, v in portfolio.coins.items() if k.lower() != "tether"}


            if days <= 2:
                label_text = ", ".join([f"{k}: {v}" for k, v in legend.items()])
                plt.plot(filter_ts, filtered_vals, label=label_text)
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.gcf().autofmt_xdate()
                plt.xlabel("Date")
                plt.ylabel("Amount")
                plt.title("Portfolio in the last 24h")
                plt.tight_layout()
                plt.legend(loc="lower right")
                plt.show()
            else:
                label_text = ", ".join([f"{k}: {v}" for k, v in legend.items()])
                plt.plot(filter_ts, filtered_vals, label=label_text)
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.gcf().autofmt_xdate()
                plt.xlabel("Date")
                plt.ylabel("Amount")
                plt.title("Portfolio")
                plt.tight_layout()
                plt.legend(loc="lower right")
                plt.show()






    async def graph_multiple_coins(self, owner_id: UUID, days: int, session: AsyncSession) -> None:
        """The method for generating a graph showing the portfolio value up to a year backwards seperated by each coin in portfolio.

            Args:
                owner_id (int): The id of the user.
                days (int): number of days backwards to track value of portfolio
                session (AsyncSession): DB session.

            Returns:
                None
        """

        async with session.begin():
            if days <= 0:
                raise HTTPException(status_code=403, detail="Number of days cant be 0 or less")

            now = datetime.now(timezone.utc)
            portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)

            total_portfolio_val = [[0] * 288 for _ in range(len(portfolio.coins))]


            days_back = int(days)

            count_fors = 0
            for crypto in portfolio.coins:
                if crypto == "tether":
                    continue
                transactions = await self.transaction_repo.show_user_transactions_between_date_by_coin(session, now - timedelta(days=days_back), now, owner_id, crypto)
                portfolio_quant = portfolio.coins.get(crypto, 0.0)

                quants = []
                for tx in transactions:
                    quants.append(tx.quantity)
                portfolio_transactions_quant = 0
                for q in quants:
                    portfolio_transactions_quant += q # 0.5
                portfolio_start_quant = portfolio_quant - portfolio_transactions_quant # 0.2

                url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
                params = {"vs_currency": "usd", "days": f"{days_back}"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["prices"]

                sorted_transactions = sorted(transactions, key=lambda x: x.date)


                prices = []
                timestamps = []
                for timestamp, price in price_usd:
                    time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                    prices.append(price * portfolio_start_quant)
                    timestamps.append(time)



                prices_usd = []
                for price in price_usd:
                    prices_usd.append(price[1])

                prices_final = []
                previous_timestamp = timestamps[0]

                for timestamp, price in zip(timestamps, prices_usd):
                    if not sorted_transactions:
                        prices_final.append(price * portfolio_start_quant)
                        previous_timestamp = timestamp
                        continue

                    if timestamp == timestamps[0]:
                        if sorted_transactions[0].date <= timestamp:
                            prices_final.append(price * (portfolio_start_quant + sorted_transactions[0].quantity))
                            sorted_transactions.remove(sorted_transactions[0])
                            portfolio_start_quant += sorted_transactions[0].quantity
                            previous_timestamp = timestamp
                        else:
                            prices_final.append(price * portfolio_start_quant)
                            previous_timestamp = timestamp
                        continue
                    elif timestamp > sorted_transactions[0].date > previous_timestamp:
                        prices_final.append(price * (portfolio_start_quant + sorted_transactions[0].quantity))
                        portfolio_start_quant += sorted_transactions[0].quantity
                        sorted_transactions.remove(sorted_transactions[0])
                        previous_timestamp = timestamp
                        continue
                    else:
                        prices_final.append(price * portfolio_start_quant)
                        previous_timestamp = timestamp


                for i in range(len(prices_final)):
                    total_portfolio_val[count_fors][i] += prices_final[i]
                count_fors += 1


            min_len = min(len(timestamps), len(total_portfolio_val[0]))
            timestamps = timestamps[:min_len - 2]
            for i in range(len(total_portfolio_val)):
                total_portfolio_val[i] = total_portfolio_val[i][:min_len - 2]



            legend = {k: round(v, 2) for k, v in portfolio.coins.items() if k.lower() != "tether"}

            for i, (coin_name, _) in enumerate(legend.items()):
                plt.plot(timestamps, total_portfolio_val[i], label=coin_name)

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.gcf().autofmt_xdate()
            plt.xlabel("Date")
            plt.ylabel("Value (USD)")
            plt.title("Portfolio coins over time")
            plt.tight_layout()
            plt.legend(loc="lower right")
            plt.show()




    # DOESNT INCLUDE SELLING IN PNL!!!!!!!!!!!!!
    async def graph_p_n_l_percent(self, owner_id: UUID, session: AsyncSession) -> None:
        """The method for generating a graph showing the portfolio profit and losses value counting from the date of the first transaction.

            Args:
                owner_id (int): The id of the user.
                session (AsyncSession): database session.

            Returns:
                None
        """

        async with session.begin():
            now = datetime.now(timezone.utc)
            transactions_general = await self.transaction_repo.show_user_transactions(session, owner_id)

            sorted_transactions = sorted([t for t in transactions_general if t.bought_price > 0],key=lambda x: x.date)
            if not sorted_transactions:
               raise HTTPException(status_code=404, detail="No purchase transactions found for the user")

            oldest_transaction = sorted_transactions[0]
            delta = now - oldest_transaction.date
            days_back = max(1.0, delta.total_seconds() / 86400.0)

            url = f"https://api.coingecko.com/api/v3/coins/{sorted_transactions[0].coin}/market_chart"
            params = {"vs_currency": "usd", "days": f"{days_back}"}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                price_usd = response.json()["prices"]



            p_n_ls_whole = np.zeros((len(sorted_transactions), len(price_usd)), dtype=float)
            p_n_ls_whole_pos = 0
            timestamps_oldest = []
            for coin in sorted_transactions:


                url = f"https://api.coingecko.com/api/v3/coins/{coin.coin}/market_chart"
                params = {"vs_currency": "usd", "days": f"{days_back}"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["prices"]

                timestamps = []
                p_n_ls = []
                for timestamp, price in price_usd:
                    time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                    timestamps.append(time)
                    p_n_ls.append(price / coin.bought_price -  1)

                if not timestamps_oldest:
                    timestamps_oldest = timestamps.copy()

                for i in range(len(p_n_ls)):
                    if coin.date > timestamps_oldest[i]:
                        p_n_ls_whole[p_n_ls_whole_pos][i] = 0.0
                    else:
                        p_n_ls_whole[p_n_ls_whole_pos][i] = p_n_ls[i]
                p_n_ls_whole[p_n_ls_whole_pos] = p_n_ls_whole[p_n_ls_whole_pos][:len(timestamps)]
                p_n_ls_whole_pos += 1





            plt.figure(figsize=(12, 6))


            for idx, coin in enumerate(sorted_transactions):
                values = np.array(p_n_ls_whole[idx], dtype=float)
                values[values == 0.0] = np.nan

                if len(values) > len(timestamps_oldest):
                    values[idx] = values[idx][:len(timestamps_oldest)]
                if len(values) < len(timestamps_oldest):
                    timestamps_oldest = timestamps_oldest[:len(values[idx])]
                plt.plot(timestamps_oldest, values, label=coin.coin)

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.gcf().autofmt_xdate()
            plt.xlabel("Date")
            plt.ylabel("PnL (%)")
            plt.title("PnL Over Time by Coin")
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.show()






    async def graph_p_n_l(self, owner_id: UUID, session: AsyncSession):
        """The method for generating a graph showing the portfolio value up to a year backwards.

            Args:
                owner_id (int): The id of the user.
                session (AsyncSession): database session.

            Returns:
                None
        """

        async with session.begin():
            transactions = await self.transaction_repo.show_user_transactions(session, owner_id)
            now = datetime.now(timezone.utc)

            sorted_transactions = sorted([t for t in transactions if t.bought_price > 0], key=lambda x: x.date)

            if not sorted_transactions:
               raise HTTPException(status_code=404, detail="No purchase transactions found for the user")
            

            oldest_transaction = sorted_transactions[0]
            delta = now - oldest_transaction.date
            days_back = max(1.0, delta.total_seconds() / 86400.0)

            url = f"https://api.coingecko.com/api/v3/coins/{sorted_transactions[0].coin}/market_chart"
            params = {"vs_currency": "usd", "days": f"{days_back}"}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                price_usd = response.json()["prices"]

            p_n_ls_whole = np.zeros((len(sorted_transactions), len(price_usd)), dtype=float)
            p_n_ls_whole_pos = 0
            timestamps_oldest = []
            for coin in sorted_transactions:
                url = f"https://api.coingecko.com/api/v3/coins/{coin.coin}/market_chart"
                params = {"vs_currency": "usd", "days": f"{days_back}"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    price_usd = response.json()["prices"]

                prices = []
                timestamps = []
                for timestamp, price in price_usd:
                    time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                    timestamps.append(time)
                    prices.append(price)

                if not timestamps_oldest:
                    timestamps_oldest = timestamps.copy()

                p_n_ls = []
                for i in prices:
                    p_n_ls.append((i * coin.quantity) - (coin.bought_price * coin.quantity))

                for i in range(len(p_n_ls)):
                    if i >= len(timestamps_oldest):
                        break
                    if timestamps_oldest[i] >= timestamps[i]:
                        p_n_ls_whole[p_n_ls_whole_pos][i] = p_n_ls[i]
                    else:
                        p_n_ls_whole[p_n_ls_whole_pos][i] = 0.0
                p_n_ls_whole_pos += 1


            concatenated_prices = np.sum(p_n_ls_whole, axis=0)

            filtered_prices = []
            filtered_ts = []
            for i in range(len(timestamps_oldest)):
                if timestamps_oldest[i] >= sorted_transactions[0].date:
                    filtered_prices.append(concatenated_prices[i])
                    filtered_ts.append(timestamps_oldest[i])


            fig, ax = plt.subplots()
            ax.plot(filtered_ts, filtered_prices)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            fig.autofmt_xdate()
            ax.set_xlabel("Date")
            ax.set_ylabel("Amount")
            ax.set_title("Profit & Loss Over Time")
            fig.tight_layout()


            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            plt.close(fig)

            return StreamingResponse(buf, media_type="image/png")





















