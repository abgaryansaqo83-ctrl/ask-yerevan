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
