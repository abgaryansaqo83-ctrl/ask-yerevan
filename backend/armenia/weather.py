# backend/armenia/weather.py

import aiohttp
import asyncio
import random
from typing import Optional

from config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
YEREVAN_LAT, YEREVAN_LON = 40.1811, 44.5136

WEATHER_EMOJIS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
}


async def get_yerevan_weather(api_key: Optional[str] = None) -> str:
    """
    Ամեն առավոտ 08:00 եղանակի հաղորդագրություն.
    Ջերմաստիճան + զգացողական + օրվա forecast + հումորային խորհուրդ.
    """
    api_key = api_key or settings.OPENWEATHER_API_KEY

    if not api_key:
        return "🌤️ Եղանակի տվյալները ժամանակավորապես անհասանելի են։ Փորձիր կրկին մի քանի րոպե հետո։"

    async with aiohttp.ClientSession() as session:
        try:
            current_url = (
                f"{OPENWEATHER_BASE_URL}/weather?"
                f"lat={YEREVAN_LAT}&lon={YEREVAN_LON}&appid={api_key}&units=metric&lang=ru"
            )

            forecast_url = (
                f"{OPENWEATHER_BASE_URL}/forecast?"
                f"lat={YEREVAN_LAT}&lon={YEREVAN_LON}&appid={api_key}&units=metric&lang=ru"
            )

            async with session.get(current_url) as resp:
                if resp.status != 200:
                    logger.error(f"OpenWeather API error: {resp.status}")
                    return "🌤️ Եղանակի տվյալները ժամանակավորապես անհասանելի են։"
                current_data = await resp.json()

            async with session.get(forecast_url) as resp:
                if resp.status != 200:
                    logger.warning("Forecast unavailable, using current data only")
                    forecast_data = None
                else:
                    forecast_data = await resp.json()

            return _format_weather_message(current_data, forecast_data)

        except Exception as e:
            logger.error(f"Weather fetch failed: {e}")
            return "🌤️ Եղանակի տվյալները ժամանակավորապես անհասանելի են։"


def _get_weather_emoji(weather_main: str) -> str:
    """Ըստ weather condition-ի emoji."""
    return WEATHER_EMOJIS.get(weather_main, "🌤️")


def _get_humor_advice(temp: float, feels_like: float, weather_main: str) -> str:
    """
    Կարճ խորհուրդ ըստ եղանակի (1 նախադասություն, փոքր emoji-ներով)։
    """
    tips = {
        "Clear": [
            "Արևոտ օր է Երևանում․ վերցրու ակնոցն ու մի քիչ քայլիր ☀️",
        ],
        "Clouds": [
            "Ամպոտ, բայց հանգիստ օր է․ տաք խմիչքը ավելորդ չէր լինի ☁️",
        ],
        "Rain": [
            "Անձրև է, անձրևանոցն ու ջրակայուն կոշիկները ցանկալի են 🌧️",
        ],
        "Drizzle": [
            "Թեթև անձրև է․ բարակ բաճկոնն ու գլխարկը բավարար է 🌦️",
        ],
        "Thunderstorm": [
            "Ամպրոպային եղանակ է․ ավելի ապահով է տանը մնալը ⛈️",
        ],
        "Snow": [
            "Ձյուն ու սառնություն․ դուրս գալիս մի շերտ ավել հագնվիր ❄️",
        ],
        "Mist": [
            "Մառախուղ է․ մեքենայով կամ ոտքով՝ մի փոքր ավելի զգույշ շարժվիր 🌫️",
        ],
        "Fog": [
            "Խիտ մառախուղ է, ճանապարհին հաշվի առ դանդաղ երթևեկությունը 🌫️",
        ],
    }

    if weather_main in tips:
        return random.choice(tips[weather_main])

    # Դեֆոլտ կարճ տարբերակներ
    if feels_like <= 0:
        return "Սառն է Երևանում․ տաք բաճկոնն ու ձեռնոցները այսօր պետք են 🧥"
    if feels_like >= 28:
        return "Տաք օր է․ ջուր խմելն ու ստվերը չմոռանաս 💧"

    return "Եղանակը համեմատաբար հանգիստ է․ քո տեմպով շարունակիր օրը 🌤️"


def _get_day_forecast_advice(min_temp: float, max_temp: float, weather_main: str) -> str:
    """Օրվա forecast-ի խորհուրդ."""
    if min_temp < 5:
        return "🌅 Առավոտյան՝ ցրտոտ է, երեկոյան՝ ավելի տաք է"
    elif max_temp > 25:
        return "🌇 Ցերեկը՝ տաք, երեկոյան՝ ավելի սառն է"
    else:
        return "🌤️ Ամբողջ օրը կայուն եղանակ"


# weather.py (_format_weather_message-ի սկզբում կամ վերևում)
WEATHER_DESC_HY = {
    "dense fog": "Խիտ մառախուղ",
    "fog": "Մառախուղ",
    "mist": "մառախուղ",
    "smoke": "ծխածածկ",
    "haze": "մեղմ մշուշ",
    "overcast clouds": "ամպամած",
    "scattered clouds": "մասնամբ ամպամած",
    "broken clouds": "ամպամածություն",
    "clear sky": "արդ և պարզ երկինք",
    # եթե API-ից ռուսերեն էլ գա, դրանց էլ կարող ես մապ անել
    "плотный туман": "Խիտ մառախուղ",
    "туман": "Մառախուղ",
}

def _format_weather_message(current: dict, forecast: Optional[dict] = None) -> str:
    temp = current["main"]["temp"]
    feels_like = current["main"]["feels_like"]
    weather_main = current["weather"][0]["main"]
    raw_desc = current["weather"][0]["description"] or ""
    city_name = current["name"]

    # ՆՈՐ՝ normalize + հայերեն
    key = raw_desc.lower()
    weather_desc = WEATHER_DESC_HY.get(key, raw_desc)

    emoji = _get_weather_emoji(weather_main)

    current_line = (
        f"{emoji} Երևան\n"
        f"🌡 Ջերմաստիճան՝ {temp:.0f}°C\n"
        f"😎 Թվում է մոտավորապես՝ {feels_like:.0f}°C\n"
        f"📝 {weather_desc}"
    )

    # Humor advice
    humor = _get_humor_advice(temp, feels_like, weather_main)

    # Day forecast
    day_forecast = ""
    if forecast and "list" in forecast and forecast["list"]:
        today_date = forecast["list"][0]["dt_txt"][:10]
        today_forecasts = [
            item for item in forecast["list"][:8]
            if item["dt_txt"].startswith(today_date)
        ]
        if today_forecasts:
            min_temp = min(item["main"]["temp_min"] for item in today_forecasts)
            max_temp = max(item["main"]["temp_max"] for item in today_forecasts)
            day_forecast = (
                f"\n📊 Օրվա կանխատեսում՝ {min_temp:.0f}°C / {max_temp:.0f}°C\n"
                f"{_get_day_forecast_advice(min_temp, max_temp, weather_main)}"
            )

    message = f"{current_line}\n\n💡 {humor}{day_forecast}"
    return message
