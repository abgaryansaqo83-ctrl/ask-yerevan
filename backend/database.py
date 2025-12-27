# backend/database.py

import sqlite3
from pathlib import Path
from datetime import date
from datetime import datetime

DB_PATH = Path("data/bot.db")

def get_connection():
    """Return a SQLite connection, auto-creates DB if missing."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # ✅ Debug log
    print(f"📂 Database path: {DB_PATH.absolute()}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Events table (միջոցառումներ, կինո, թատրոն, ֆեստիվալներ)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT,
            time TEXT,
            place TEXT,
            city TEXT,
            category TEXT,
            url TEXT,
            source TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT,
            created_at TEXT
        )
        """
    )

    # Violations table (կանոնների խախտումներ)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            vtype TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    # ✅ News table (նորություններ)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_hy TEXT NOT NULL,
            title_en TEXT NOT NULL,
            content_hy TEXT NOT NULL,
            content_en TEXT NOT NULL,
            image_url TEXT,
            published INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    # Memory table (optional future use)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            key TEXT,
            value TEXT,
            updated_at TEXT
        )
        """
    )

    # Listings table (հայտարարություններ)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            thread_id TEXT,
            user_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    conn.commit()
    conn.close()


# ------------ User helpers ------------

def save_user(chat_id, username=None, first_name=None, last_name=None, language="hy"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO users(chat_id, username, first_name, last_name, language, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (chat_id, username, first_name, last_name, language),
    )

    conn.commit()
    conn.close()


def get_user(chat_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    row = cur.fetchone()
    conn.close()
    return row

# ------------ Events helpers ------------

def save_event(event: dict) -> int:
    """
    event: dict(title, date, time, place, city, category, url, source)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO events (title, date, time, place, city, category, url, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.get("title"),
            event.get("date"),
            event.get("time"),
            event.get("place"),
            event.get("city"),
            event.get("category"),
            event.get("url"),
            event.get("source"),
        ),
    )
    event_id = cur.lastrowid
    conn.commit()
    conn.close()
    return event_id


def get_upcoming_events(limit: int = 20, city: str | None = None, category: str | None = None):
    """
    Վերադարձնում է մոտակա event-ները՝ optional քաղաք / category ֆիլտրով։
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT * FROM events
        WHERE date IS NOT NULL
          AND datetime(date) >= date('now')
        """
    params: list[str] = []

    if city:
        query += " AND city = ?"
        params.append(city)
    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY date, time LIMIT ?"
    params.append(str(limit))

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def cleanup_old_events(days: int = 30) -> None:
    """
    Ջնջում է event-ները, որոնք արդեն հին են (օր. 30 օր).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM events
        WHERE datetime(date) < datetime('now', ?)
        """,
        (f"-{days} days",),
    )
    conn.commit()
    conn.close()

def get_today_events(city: str | None = None, category: str | None = None):
    """
    Վերադարձնում է միայն տվյալ օրվա event-ները (date == այսօր),
    optional քաղաք / category ֆիլտրերով։
    """
    today = date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM events WHERE date = ?"
    params: list[str] = [today]

    if city:
        query += " AND city = ?"
        params.append(city)
    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY time"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# ------------ News helpers ------------

def save_news(title_hy: str, title_en: str, content_hy: str, content_en: str, image_url: str | None = None) -> int:
    """
    Ավելացնում է նոր նորություն news table‑ում։
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO news (title_hy, title_en, content_hy, content_en, image_url, published)
        VALUES (?, ?, ?, ?, ?, 1)
        """,
        (title_hy, title_en, content_hy, content_en, image_url),
    )
    news_id = cur.lastrowid
    conn.commit()
    conn.close()
    return news_id


def get_all_news(limit: int = 10):
    """
    Վերադարձնում է վերջին հրապարակված նորությունները։
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM news
        WHERE published = 1
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ------------ Listings helpers ------------

def save_listing(category: str, chat_id: int, thread_id: int | None,
                 user_id: int, message_id: int, text: str) -> int:
    """
    Պահում է մեկ հայտարարություն listings table-ում և վերադարձնում է դրա id-ն։
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO listings (category, chat_id, thread_id, user_id, message_id, text)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (category, str(chat_id), str(thread_id) if thread_id is not None else None,
         str(user_id), str(message_id), text),
    )
    listing_id = cur.lastrowid
    conn.commit()
    conn.close()
    return listing_id


def cleanup_old_listings(days: int = 15) -> None:
    """
    Ջնջում է listings, որոնք ավելի հին են, քան `days` օր։
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM listings
        WHERE datetime(created_at) < datetime('now', ?)
        """,
        (f"-{days} days",),
    )
    conn.commit()
    conn.close()

def count_similar_listings(user_id: int, text: str, days: int = 15) -> int:
    """
    Հաշվում է, քանի հայտարարություն է նույն user-ը հրապարակել վերջին `days` օրում,
    որտեղ text-ը նույնն է կամ շատ նման (պարզ տարբերակ՝ հավասար կամ LIKE).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*) AS cnt
        FROM listings
        WHERE user_id = ?
          AND datetime(created_at) >= datetime('now', ?)
          AND text = ?
        """,
        (str(user_id), f"-{days} days", text),
    )
    row = cur.fetchone()
    conn.close()
    return int(row["cnt"] if row else 0)


# ------------ Violations helpers ------------

def register_violation(user_id: int, chat_id: int, vtype: str) -> None:
    """
    Գրանցում է մեկ խախտում տվյալ օգտվողի համար.
    vtype: 'spam_politics' / 'aggressive_chat' / 'repeat_listing'
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO violations (user_id, chat_id, vtype)
        VALUES (?, ?, ?)
        """,
        (str(user_id), str(chat_id), vtype),
    )
    conn.commit()
    conn.close()


def count_violations(user_id: int, chat_id: int, vtype: str, within_hours: int) -> int:
    """
    Հաշվում է, քանի նույն type-ի խախտում ունի user-ը վերջին within_hours ժամերում
    տվյալ chat-ում։
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*) AS cnt
        FROM violations
        WHERE user_id = ?
          AND chat_id = ?
          AND vtype = ?
          AND datetime(created_at) >= datetime('now', ?)
        """,
        (str(user_id), str(chat_id), vtype, f"-{within_hours} hours"),
    )
    row = cur.fetchone()
    conn.close()
    return int(row["cnt"] if row else 0)
