import requests


class WeatherAPI:
    """Premium hava durumu API'si (OpenWeatherMap)
    
    API key: https://openweathermap.org/api (free tier: 60 sorgu/dakika)
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def get_weather(self, city: str = "Istanbul", country_code: str = "") -> str:
        if not self.api_key:
            return "Hava durumu API anahtari tanimlanmamis. `steph credentials set weather API_KEY`"
        try:
            q = city
            if country_code:
                q += f",{country_code}"
            r = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": q, "appid": self.api_key, "units": "metric", "lang": "tr"},
                timeout=10,
            )
            if r.status_code == 401:
                return "Gecersiz API anahtari."
            if r.status_code == 404:
                return f"Sehir bulunamadi: {city}"
            data = r.json()
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            wind = data["wind"]["speed"]
            return (
                f"{city} Hava Durumu:\n"
                f"{desc}\n"
                f"Sicaklik: {temp:.1f}C (hissedilen: {feels:.1f}C)\n"
                f"Nem: %{humidity}\n"
                f"Ruzgar: {wind} m/s"
            )
        except requests.exceptions.Timeout:
            return "Hava durumu API'ye ulasilamadi (zaman asimi)."
        except Exception as e:
            return f"Hava durumu alinamadi: {e}"

    def get_forecast(self, city: str = "Istanbul") -> str:
        if not self.api_key:
            return "API anahtari yok."
        try:
            r = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={"q": city, "appid": self.api_key, "units": "metric", "lang": "tr", "cnt": 8},
                timeout=10,
            )
            if r.status_code != 200:
                return f"Hata: {r.status_code}"
            data = r.json()
            lines = [f"{city} 5 Gunluk Tahmin:"]
            for item in data["list"][::2]:
                dt = item["dt_txt"][:16]
                t = item["main"]["temp"]
                desc = item["weather"][0]["description"]
                lines.append(f"  {dt}  {t:.1f}C  {desc}")
            return "\n".join(lines)
        except Exception as e:
            return f"Tahmin alinamadi: {e}"
