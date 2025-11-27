import logging
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure main logger
logger = logging.getLogger("ask_yerevan")
logger.setLevel(logging.INFO)

# File handler — saves logs to logs/bot.log
file_handler = logging.FileHandler(f"{LOG_DIR}/bot.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Console handler — shows logs in console (Render dashboard)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
