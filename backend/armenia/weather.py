# backend/armenia/weather.py

import aiohttp
import asyncio
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
            # Current weather
            current_url = (
                f"{OPENWEATHER_BASE_URL}/weather?"
                f"lat={YEREVAN_LAT}&lon={YEREVAN_LON}&appid={api_key}&units=metric&lang=ru"
            )
            
            # 5-day forecast (մենք օգտագործում ենք առաջին օրվա min/max)
            forecast_url = (
                f"{OPENWEATHER_BASE_URL}/forecast?"
                f"lat={YEREVAN_LAT}&lon={YEREVAN_LON}&appid={api_key}&units=metric&lang=ru"
            )

            # Current weather
            async with session.get(current_url) as resp:
                if resp.status != 200:
                    logger.error(f"OpenWeather API error: {resp.status}")
                    return "🌤️ Եղանակի տվյալները ժամանակավորապես անհասանելի են։"
                
                current_data = await resp.json()

            # Forecast (այսօրվա min/max)
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
    Օրվա հումորային խորհուրդ՝ ըստ եղանակի.
    """
    humor_tips = {
        "Clear": "Հիշիր արևային ակնոցդ, որ մարդիկ չտեսնեն, թե որքան քիչ ես քնած 😎☀️",
        "Clouds": "Մի անհանգստացիր, դա պարզապես բնության «ֆիլտրն» է՝ քեզ ավելի լուսանկարչական դարձնելու համար ☁️📸",
        "Rain": "Հիշիր, որ նույնիսկ ամպերն են երբեմն լացում։ Թույլ տուր նրանց, բայց դու քեզ համար սարքիր տաք թեյ ☕🌧️",
        "Thunderstorm": "Մնա տանը, դա բնության DJ-ն ա նվագում ⛈️🎶",
        "Snow": "Հագնվի՛ր շերտերով․ միակ layering-ը, որը երբեք չի դուրս գալիս մոդայից ❄️🧥",
        "Mist": "Լավ պահի՛ր գլխարկդ։ Եթե չես պահում, ուրեմն դա այլևս գլխարկ չէ, դա թռչող օբյեկտ է 🌫️🎩",
    }
    
    # Եթե weather_main չկա dictionary-ում, ընտրում ենք temp-ի հիման վրա
    tip = humor_tips.get(weather_main, "Բարի օր քեզ և եղանակից անկախ՝ լավ տրամադրություն 🌤️😊")
    
    return tip

def _get_day_forecast_advice(min_temp: float, max_temp: float, weather_main: str) -> str:
    """Օրվա forecast-ի խորհուրդ."""
    if min_temp < 5:
        return "🌅 Առավոտը սառը, երեկոյան տաքանում ա"
    elif max_temp > 25:
        return "🌇 Ցերեկը տաք, երեկոյան հովանա"
    else:
        return "🌤️ Ամբողջ օրը կայուն եղանակ"


def _format_weather_message(current: dict, forecast: Optional[dict] = None) -> str:
    """Հաղորդագրության ֆորմատավորում."""
    temp = current["main"]["temp"]
    feels_like = current["main"]["feels_like"]
    weather_main = current["weather"][0]["main"]
    weather_desc = current["weather"][0]["description"]
    city_name = current["name"]
    
    emoji = _get_weather_emoji(weather_main)
    
    # Current weather
    current_line = (
        f"{emoji} "{city_name}"
        f"🌡️ Ջերմաստիճան՝ {temp:.0f}°C\n"
        f"😎 Զգացողական՝ {feels_like:.0f}°C\n"
        f"📝 {weather_desc.title()}"
    )
    
    # Humor advice
    humor = _get_humor_advice(temp, feels_like, weather_main)
    
    # Day forecast
    day_forecast = ""
    if forecast:
        # Օրվա min/max temperature-ները առաջին 8 ժամից (այսօր)
        today_forecasts = [
            item for item in forecast["list"][:8] 
            if item["dt_txt"].startswith(forecast["list"][0]["dt_txt"][:10])
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

