# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Telegram Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # OpenWeather
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")

    # AI / GPT
    AI_API_KEY: str = os.getenv("AI_API_KEY")

    # Project settings
    PROJECT_NAME: str = "AskYerevan"
    VERSION: str = "1.0.0"

settings = Settings()
