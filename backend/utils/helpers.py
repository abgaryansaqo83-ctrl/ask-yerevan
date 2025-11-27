import json
import re
from datetime import datetime

# -----------------------------
# Time helpers
# -----------------------------

def now():
    """Return current datetime (UTC+4 for Armenia)."""
    return datetime.utcnow()  # Render uses UTC; later we can convert if needed


def format_time(ts=None):
    """Format datetime nicely."""
    ts = ts or now()
    return ts.strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Text helpers
# -----------------------------

def clean_text(text: str) -> str:
    """Cleanup incoming text from Telegram."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def shorter(text: str, limit: int = 250) -> str:
    """Shorten long text."""
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


# -----------------------------
# JSON helpers
# -----------------------------

def load_json(path: str):
    """Load JSON file safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path: str, data: dict):
    """Save dict → JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------------
# Telegram helpers
# -----------------------------

def mask_token(token: str) -> str:
    """Hide sensitive token."""
    if len(token) < 10:
        return "***"
    return token[:6] + "***" + token[-4:]

