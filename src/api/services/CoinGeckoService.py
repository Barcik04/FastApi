# src/api/services/CoinGeckoService.py

import httpx

class CoinGeckoService:
    BASE_URL = "https://api.coingecko.com/api/v3"

    async def get_coin_price(self, coin_id: str):
        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
