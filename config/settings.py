import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")
    AI_API_KEY: str = os.getenv("AI_API_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()
