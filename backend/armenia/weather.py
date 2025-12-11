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
    Օրվա հումորային խորհուրդ՝ ըստ եղանակի, randomized տարբերակներով։
    """
    tips = {
        "Clear": [
            "Արևը ժպտում է, ուրեմն այսօր կարող եք էլի ձևացնել, թե ամեն ինչ վերահսկողության տակ է։ Լրիվ սուտ է, բայց արևն էլ չի իմանա 😎☀️",
        ],
        "Clouds": [
            "Եթե օրը պայծառ չէ, մի նեղսրտեք, պարզապես եղեք «միստիկ» ու «խորհրդավոր», ոչ թե «ներկառուցված Wi‑Fi չունեցող մարդ» ☁️📶",
        ],
        "Rain": [
            "Վերցրեք ամենամեծ անձրևանոցը, ոչ թե անձրևից պաշտպանվելու, այլ հոգու խաղաղության համար — մեծ անձրևանոցով մարդուն ոչ ոք հարցեր չի տալիս 🌧️☂️",
        ],
        "Thunderstorm": [
            "Եթե փոթորիկ է — մնա տանը, դա բնության DJ-ն է նվագում ⛈️🎶",
        ],
        "Snow": [
            "Եթե այսօր ձյուն է, ապա ամեն ինչ թույլատրված է. աշխատանքի ուշ գնալ, տանը շոկոլադ ուտել ու անդադար բողոքել՝ «էս ինչ ա էս ինչ անտանելի ձմեռ ա» ❄️🍫",
        ],
        "Mist": [
            "Էսօր փողոց դուրս գաս, ուր գնաս՝ չես իմանա… բայց գոնե երևակայությունդ կզարգանա։ Եթե գործից ուշանաս, ասա՝ «վա՜յ մոլորվել էի» 🌫️🙂",
            "Տեսանելիությունը քիչ է, բայց լավ կողմն էն ա, որ ոչ ոք չի տեսնի, թե ինչ հավես գիշերանոցով ես դուրս եկել 🌫️🛌",
            "Քաղաքը դարձել է ռեալ «միստերի» ֆիլմ։ Մի քիչ էլ, ու ինքդ քեզ կմոռանաս, բայց կարևորն էն ա, որ Wi‑Fi-ը կա 🌫️📡",
        ],
    }

    if weather_main in tips:
        return random.choice(tips[weather_main])

    return "Բարի օր քեզ և եղանակից անկախ՝ լավ տրամադրություն 🌤️😊"


def _get_day_forecast_advice(min_temp: float, max_temp: float, weather_main: str) -> str:
    """Օրվա forecast-ի խորհուրդ."""
    if min_temp < 5:
        return "🌅 Առավոտյան՝ սառը, երեկոյան՝ տաքանում է"
    elif max_temp > 25:
        return "🌇 Ցերեկը՝ տաք, երեկոյան՝ ավելի զով"
    else:
        return "🌤️ Ամբողջ օրը կայուն եղանակ"


def _format_weather_message(current: dict, forecast: Optional[dict] = None) -> str:
    temp = current["main"]["temp"]
    feels_like = current["main"]["feels_like"]
    weather_main = current["weather"][0]["main"]
    weather_desc = current["weather"][0]["description"]
    city_name = current["name"]

    emoji = _get_weather_emoji(weather_main)

    current_line = (
        f"{emoji} {city_name}\n"
        f"🌡️ Ջերմաստիճան՝ {temp:.0f}°C\n"
        f"😎 Զգացողություն՝ {feels_like:.0f}°C\n"
        f"📝 {weather_desc.title()}"
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
