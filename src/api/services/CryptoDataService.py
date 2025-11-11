from datetime import datetime, timedelta, timezone

import httpx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from uuid import UUID

from fastapi import HTTPException

from src.api.models.CryptoDataOrm import CryptoDataOrm
from src.api.repositories.PortfolioRepository import PortfolioRepository
from src.api.repositories.TransactionRepository import TransactionRepository
from src.db import SessionLocal
from src.api.repositories.CryptoDataRepository import CryptoDataRepository


class CryptoDataService:
    def __init__(
            self,
            repo: CryptoDataRepository | None = None,
            transaction_repo: TransactionRepository | None = None,
            portfolio_repo: PortfolioRepository | None = None,
    ):
        self.repo = repo or CryptoDataRepository()
        self.transaction_repo = transaction_repo or TransactionRepository()
        self.portfolio_repo = portfolio_repo or PortfolioRepository()


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


    async def graph_last_24h(self, owner_id: UUID, days: int) -> None:
        async with SessionLocal() as session:
            async with session.begin():
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
                        total_portfolio_val[i] += prices_final[i]


                if len(timestamps) != len(total_portfolio_val):
                    total_portfolio_val = total_portfolio_val[:len(timestamps)]

                legend = {k: round(v, 3) for k, v in portfolio.coins.items() if k.lower() != "tether"}


                if days <= 2:
                    label_text = ", ".join([f"{k}: {v}" for k, v in legend.items()])
                    plt.plot(timestamps, total_portfolio_val, label=label_text)
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
                    plt.plot(timestamps, total_portfolio_val, label=label_text)
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                    plt.gcf().autofmt_xdate()
                    plt.xlabel("Date")
                    plt.ylabel("Amount")
                    plt.title("Portfolio in the last 24h")
                    plt.tight_layout()
                    plt.legend(loc="lower right")
                    plt.show()






    async def tests(self, days: int) -> None:
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": days}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            list_len = len(response.json()["prices"])

        print(list_len)




    async def graph_multiple_coins(self, owner_id: UUID, days: int) -> None:
        async with SessionLocal() as session:
            async with session.begin():
                now = datetime.now(timezone.utc)
                portfolio = await self.portfolio_repo.show_user_portfolio(session, owner_id)

                total_portfolio_val = [[0] * 284 for _ in range(len(portfolio.coins))]


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

                for i in range(len(total_portfolio_val)):
                    total_portfolio_val[i] = total_portfolio_val[i][:len(timestamps)]


                if len(timestamps) != len(total_portfolio_val[0]):
                    total_portfolio_val = total_portfolio_val[:len(timestamps)]



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



    async def graph_p_n_l_percent(self, owner_id: UUID) -> None:
        async with SessionLocal() as session:
            async with session.begin():
                now = datetime.now(timezone.utc)
                transactions_general = await self.transaction_repo.show_user_transactions(session, owner_id)

                unique_coins = sorted({t.coin for t in transactions_general})

                sorted_transactions = sorted(transactions_general, key=lambda x: x.date)
                oldest_transaction = sorted_transactions[0]
                delta = now - oldest_transaction.date
                days_back = max(1.0, delta.total_seconds() / 86400.0)


                for coin in unique_coins:
                    tx_coin_all = [t for t in transactions_general if t.coin == coin]
                    tx_coin_all.sort(key=lambda x: x.date)

                    delta = now - tx_coin_all[0].date
                    days_back_t = max(1.0, delta.total_seconds() / 86400.0)

                    transactions = await self.transaction_repo.show_user_transactions_between_date_by_coin(
                        session,
                        now - timedelta(days=days_back_t),
                        now,
                        owner_id,
                        coin,
                    )

                    sorted_transactions = sorted(transactions, key=lambda x: x.date)

                    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
                    params = {"vs_currency": "usd", "days": f"{days_back}"}

                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params)
                        response.raise_for_status()
                        price_usd = response.json()["prices"]

                    timestamps = []
                    prices = []
                    for timestamp, price in price_usd:
                        time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                        timestamps.append(time)
                        prices.append(price)



                    price_saved = sorted_transactions[0].bought_price
                    p_n_ls = [1 - (sorted_transactions[0].bought_price / prices[0])] # -0.11

                    sorted_transactions.pop(0)
                    sorted_transactions_operate = sorted_transactions.copy()

                    store_avg_tr = [price_saved * sorted_transactions_operate[0].quantity] # 2 * 85 000  ## 3 * 105 000
                    quantity_all = sorted_transactions_operate[0].quantity # 2


                    for i in range(len(prices)):
                        if sorted_transactions_operate and not timestamps[i - 1] < sorted_transactions_operate[0].date < timestamps[i]:
                            avg_whole = sum(store_avg_tr) / quantity_all
                            p_n_ls.append((prices[i] / avg_whole) - 1)
                            continue
                        while sorted_transactions_operate and timestamps[i - 1] < sorted_transactions_operate[0].date < timestamps[i]:
                            quantity_all += sorted_transactions_operate[0].quantity
                            store_avg_tr.append(sorted_transactions_operate[0].bought_price * sorted_transactions_operate[0].quantity) # 105 * 3
                            avg_whole = sum(store_avg_tr) / quantity_all

                            p_n_ls.append((prices[i] / avg_whole) - 1) # 0
                            sorted_transactions_operate.pop(0)

                        else:
                            avg_whole = sum(store_avg_tr) / quantity_all
                            p_n_ls.append((prices[i] / avg_whole) - 1)


                    print("prices\n\n\n\n")
                    for i in p_n_ls:
                        print(i)

















