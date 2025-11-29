import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file (locally). On Render values գալիս են Environment-ից.
load_dotenv()


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")
    GOOGLE_DIRECTIONS_KEY: str = os.getenv("GOOGLE_DIRECTIONS_KEY")
    AI_API_KEY: str = os.getenv("AI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Yerevan")
    GROUP_CHAT_ID: int = int(os.getenv("GROUP_CHAT_ID", "-1003340745236"))
    ADMIN_CHAT_ID=8233762189


settings = Settings()
