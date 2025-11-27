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

