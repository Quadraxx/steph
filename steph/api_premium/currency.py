import requests


class CurrencyAPI:
    """Premium doviz kuru API'si (ExchangeRate-API / OpenExchangeRates)
    
    API key: https://www.exchangerate-api.com (free tier: 1500 sorgu/ay)
    veya https://openexchangerates.org
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def get_rate(self, from_cur: str = "USD", to_cur: str = "TRY") -> str:
        if not self.api_key:
            return "Doviz API anahtari tanimlanmamis."
        try:
            r = requests.get(
                f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_cur}/{to_cur}",
                timeout=10,
            )
            if r.status_code != 200:
                return f"Doviz kuru alinamadi (kod: {r.status_code})"
            data = r.json()
            rate = data["conversion_rate"]
            return f"1 {from_cur} = {rate:.4f} {to_cur}"
        except Exception as e:
            return f"Kur alinamadi: {e}"

    def get_rates(self, base: str = "TRY") -> str:
        if not self.api_key:
            return "Doviz API anahtari yok."
        try:
            r = requests.get(
                f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{base}",
                timeout=10,
            )
            if r.status_code != 200:
                return f"Doviz kuru alinamadi"
            data = r.json()
            rates = data["conversion_rates"]
            majors = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
            lines = [f"Guncel Kurlar (baz: {base}):"]
            for cur in majors:
                if cur in rates:
                    lines.append(f"  {cur}: {rates[cur]:.4f}")
            return "\n".join(lines)
        except Exception as e:
            return f"Kurlar alinamadi: {e}"
