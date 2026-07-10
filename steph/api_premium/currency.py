import requests


class CurrencyAPI:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def available(self) -> bool:
        return True

    def get_rate(self, from_cur: str = "USD", to_cur: str = "TRY") -> str:
        if self.api_key:
            return self._get_rate_premium(from_cur, to_cur)
        return self._get_rate_free(from_cur, to_cur)

    def get_rates(self, base: str = "TRY") -> str:
        if self.api_key:
            return self._get_rates_premium(base)
        return self._get_rates_free(base)

    def _get_rate_free(self, from_cur: str, to_cur: str) -> str:
        try:
            r = requests.get(
                f"https://open.er-api.com/v6/latest/{from_cur}",
                timeout=10,
            )
            if r.status_code != 200:
                return f"Kur alinamadi."
            data = r.json()
            if data.get("result") == "success" and to_cur in data.get("rates", {}):
                rate = data["rates"][to_cur]
                return f"1 {from_cur} = {rate:.4f} {to_cur}"
            return f"Kur alinamadi."
        except Exception as e:
            return f"Kur alinamadi."

    def _get_rate_premium(self, from_cur: str, to_cur: str) -> str:
        try:
            r = requests.get(
                f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_cur}/{to_cur}",
                timeout=10,
            )
            if r.status_code != 200:
                return self._get_rate_free(from_cur, to_cur)
            data = r.json()
            rate = data["conversion_rate"]
            return f"1 {from_cur} = {rate:.4f} {to_cur}"
        except:
            return self._get_rate_free(from_cur, to_cur)

    def _get_rates_free(self, base: str) -> str:
        try:
            r = requests.get(
                f"https://open.er-api.com/v6/latest/{base}",
                timeout=10,
            )
            if r.status_code != 200:
                return "Kurlar alinamadi."
            data = r.json()
            if data.get("result") != "success":
                return "Kurlar alinamadi."
            rates = data.get("rates", {})
            majors = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
            lines = [f"Guncel Kurlar (baz: {base}):"]
            for cur in majors:
                if cur in rates:
                    lines.append(f"  {cur}: {rates[cur]:.4f}")
            return "\n".join(lines)
        except Exception as e:
            return f"Kurlar alinamadi."

    def _get_rates_premium(self, base: str) -> str:
        try:
            r = requests.get(
                f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{base}",
                timeout=10,
            )
            if r.status_code != 200:
                return self._get_rates_free(base)
            data = r.json()
            rates = data["conversion_rates"]
            majors = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
            lines = [f"Guncel Kurlar (baz: {base}):"]
            for cur in majors:
                if cur in rates:
                    lines.append(f"  {cur}: {rates[cur]:.4f}")
            return "\n".join(lines)
        except:
            return self._get_rates_free(base)
