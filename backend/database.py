# backend/database.py

import sqlite3
from pathlib import Path

DB_PATH = Path("data/bot.db")


def get_connection():
    """Return a SQLite connection, auto-creates DB if missing."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

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
            vtype TEXT NOT NULL,          -- spam_politics / aggressive_chat / repeat_listing
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
            category TEXT NOT NULL,           -- sell / rent / job_offer / service_offer / search
            chat_id TEXT NOT NULL,
            thread_id TEXT,                   -- optional, if using topics
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

