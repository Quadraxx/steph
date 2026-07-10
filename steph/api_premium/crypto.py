import requests


class CryptoAPI:
    """Premium kripto para API'si (CoinGecko / CoinMarketCap)
    
    CoinGecko: ucretsiz (API key opsiyonel)
    CoinMarketCap: https://pro.coinmarketcap.com (free tier: 10k sorgu/ay)
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def available(self) -> bool:
        return True

    def get_price(self, coin: str = "bitcoin", currency: str = "usd") -> str:
        try:
            headers = {}
            if self.api_key:
                headers["X-CMC_PRO_API_KEY"] = self.api_key
            r = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin.lower(), "vs_currencies": currency.lower()},
                headers=headers,
                timeout=10,
            )
            if r.status_code != 200:
                return f"Fiyat alinamadi (kod: {r.status_code})"
            data = r.json()
            if coin.lower() not in data:
                return f"Coin bulunamadi: {coin}"
            price = data[coin.lower()][currency.lower()]
            return f"{coin.upper()} = {price:.2f} {currency.upper()}"
        except Exception as e:
            return f"Kripto fiyat alinamadi: {e}"

    def get_top(self, limit: int = 10, currency: str = "usd") -> str:
        try:
            r = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": currency.lower(),
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": False,
                },
                timeout=10,
            )
            if r.status_code != 200:
                return f"Liste alinamadi"
            data = r.json()
            lines = [f"Top {limit} Kripto Para ({currency.upper()}):"]
            for i, coin in enumerate(data, 1):
                name = coin["name"]
                price = coin["current_price"]
                change = coin.get("price_change_percentage_24h", 0)
                arrow = "📈" if change and change > 0 else "📉"
                change_str = f"%{change:.1f}" if change else "N/A"
                lines.append(f"  {i}. {name:15} {price:>10.2f} {arrow} {change_str}")
            return "\n".join(lines)
        except Exception as e:
            return f"Kripto listesi alinamadi: {e}"
