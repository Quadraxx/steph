import requests


class WeatherAPI:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def available(self) -> bool:
        return True

    def get_weather(self, city: str = "Istanbul", country_code: str = "") -> str:
        if self.api_key:
            return self._get_premium(city, country_code)
        return self._get_free(city)

    def get_forecast(self, city: str = "Istanbul") -> str:
        if self.api_key:
            return self._get_forecast_premium(city)
        return self._get_forecast_free(city)

    def _get_free(self, city: str) -> str:
        try:
            r = requests.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=10,
                headers={"User-Agent": "curl"}
            )
            if r.status_code == 200:
                data = r.json()
                current = data["current_condition"][0]
                temp = current["temp_C"]
                desc = current["weatherDesc"][0]["value"]
                humidity = current["humidity"]
                wind = current["windspeedKmph"]
                return f"{city}: {desc}, {temp}C, nem: %{humidity}, ruzgar: {wind}km/s"
            return f"{city} icin hava durumu alinamadi."
        except:
            return f"Hava durumu alinamadi."

    def _get_premium(self, city: str, country: str = "") -> str:
        try:
            q = city
            if country:
                q += f",{country}"
            r = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": q, "appid": self.api_key, "units": "metric", "lang": "tr"},
                timeout=10,
            )
            if r.status_code == 401:
                return "Gecersiz API anahtari. Ucretsiz kullanim icin API key'i bos birak."
            if r.status_code == 404:
                return f"Sehir bulunamadi: {city}"
            data = r.json()
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            wind = data["wind"]["speed"]
            return (
                f"{city}: {desc}, {temp:.1f}C (hissedilen: {feels:.1f}C), "
                f"nem: %{humidity}, ruzgar: {wind}m/s"
            )
        except requests.exceptions.Timeout:
            return "Hava durumu API'ye ulasilamadi."
        except Exception as e:
            return f"Hata: {e}"

    def _get_forecast_free(self, city: str) -> str:
        try:
            r = requests.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=10,
                headers={"User-Agent": "curl"}
            )
            if r.status_code == 200:
                data = r.json()
                lines = [f"{city} Tahmin:"]
                for day in data["weather"][:3]:
                    date = day["date"]
                    t_max = day["maxtempC"]
                    t_min = day["mintempC"]
                    desc = day["hourly"][0]["weatherDesc"][0]["value"]
                    lines.append(f"  {date}: {desc}, {t_min}-{t_max}C")
                return "\n".join(lines)
            return "Tahmin alinamadi."
        except:
            return "Tahmin alinamadi."

    def _get_forecast_premium(self, city: str) -> str:
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
