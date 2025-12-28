# backend/database.py

import os
from pathlib import Path
from datetime import date, datetime

# Check if PostgreSQL URL is available
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL mode
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    def get_connection():
        """Return a PostgreSQL connection"""
        print(f"🐘 Using PostgreSQL: {DATABASE_URL[:30]}...")
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    
    def get_cursor(conn):
        """Return a dict cursor for PostgreSQL"""
        return conn.cursor(cursor_factory=RealDictCursor)

else:
    # SQLite mode (fallback for local development)
    import sqlite3
    
    DB_PATH = Path("data/bot.db")
    
    def get_connection():
        """Return a SQLite connection, auto-creates DB if missing."""
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        print(f"📂 Using SQLite: {DB_PATH.absolute()}")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_cursor(conn):
        """Return a cursor for SQLite"""
        return conn.cursor()


def init_db():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cur = get_cursor(conn)
    
    # Determine SQL syntax based on database type
    if DATABASE_URL:
        # PostgreSQL syntax
        autoincrement = "SERIAL PRIMARY KEY"
        datetime_now = "CURRENT_TIMESTAMP"
        bool_type = "BOOLEAN"
        placeholder = "%s"
    else:
        # SQLite syntax
        autoincrement = "INTEGER PRIMARY KEY AUTOINCREMENT"
        datetime_now = "datetime('now')"
        bool_type = "INTEGER"
        placeholder = "?"
    
    # Events table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS events (
            id {autoincrement},
            title TEXT NOT NULL,
            date TEXT,
            time TEXT,
            place TEXT,
            city TEXT,
            category TEXT,
            url TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)
    
    # Users table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id {autoincrement},
            chat_id TEXT UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT,
            created_at TIMESTAMP
        )
    """)
    
    # Violations table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS violations (
            id {autoincrement},
            user_id TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            vtype TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)
    
    # News table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS news (
            id {autoincrement},
            title_hy TEXT NOT NULL,
            title_en TEXT NOT NULL,
            content_hy TEXT NOT NULL,
            content_en TEXT NOT NULL,
            image_url TEXT,
            category TEXT DEFAULT 'general',  -- ← Նոր column
            published {bool_type} DEFAULT {'TRUE' if DATABASE_URL else '1'},
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)
    
    # Memory table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS memory (
            id {autoincrement},
            chat_id TEXT,
            key TEXT,
            value TEXT,
            updated_at TIMESTAMP
        )
    """)
    
    # Listings table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS listings (
            id {autoincrement},
            category TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            thread_id TEXT,
            user_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")


# ------------ User helpers ------------

def save_user(chat_id, username=None, first_name=None, last_name=None, language="hy"):
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO users(chat_id, username, first_name, last_name, language, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (chat_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                language = EXCLUDED.language
            """,
            (chat_id, username, first_name, last_name, language),
        )
    else:
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
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    else:
        cur.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    
    row = cur.fetchone()
    conn.close()
    return row


# ------------ Events helpers ------------

def save_event(event: dict) -> int:
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO events (title, date, time, place, city, category, url, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING id
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
        result = cur.fetchone()
        event_id = result['id'] if result else None
    else:
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
    conn = get_connection()
    cur = get_cursor(conn)
    
    query = """
        SELECT * FROM events
        WHERE date IS NOT NULL
          AND date >= CURRENT_DATE
    """ if DATABASE_URL else """
        SELECT * FROM events
        WHERE date IS NOT NULL
          AND datetime(date) >= date('now')
    """
    
    params = []
    
    if city:
        query += " AND city = " + ("%s" if DATABASE_URL else "?")
        params.append(city)
    if category:
        query += " AND category = " + ("%s" if DATABASE_URL else "?")
        params.append(category)
    
    query += " ORDER BY date, time LIMIT " + ("%s" if DATABASE_URL else "?")
    params.append(limit)
    
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def cleanup_old_events(days: int = 30) -> None:
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            DELETE FROM events
            WHERE date < CURRENT_DATE - INTERVAL '%s days'
            """,
            (days,),
        )
    else:
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
    today = date.today().isoformat()
    conn = get_connection()
    cur = get_cursor(conn)
    
    query = "SELECT * FROM events WHERE date = " + ("%s" if DATABASE_URL else "?")
    params = [today]
    
    if city:
        query += " AND city = " + ("%s" if DATABASE_URL else "?")
        params.append(city)
    if category:
        query += " AND category = " + ("%s" if DATABASE_URL else "?")
        params.append(category)
    
    query += " ORDER BY time"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# ------------ News helpers ------------

def save_news(
    title_hy, title_en, content_hy, content_en,
    image_url=None, category="general", source_url=None,
    event_date=None,      # ✅ ՆՈՌ
    event_time=None,      # ✅ ՆՈՌ
    venue_hy=None,        # ✅ ՆՈՌ
    venue_en=None,        # ✅ ՆՈՌ
    price_hy=None,        # ✅ ՆՈՌ
    price_en=None,        # ✅ ՆՈՌ
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO news (
                    title_hy,
                    title_en,
                    content_hy,
                    content_en,
                    image_url,
                    category,
                    source_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_url) DO NOTHING;
                """,
                (
                    title_hy,
                    title_en,
                    content_hy,
                    content_en,
                    image_url,
                    category,
                    source_url,
                ),
            )

def get_all_news(limit: int = 10, category: str | None = None):
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        base_query = """
            SELECT * FROM news
            WHERE published = TRUE
              AND created_at >= NOW() - INTERVAL '6 months'
        """
        params = []

        if category:
            base_query += " AND category = %s"
            params.append(category)

        base_query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(base_query, tuple(params))
    else:
        base_query = """
            SELECT * FROM news
            WHERE published = 1
              AND created_at >= datetime('now', '-6 months')
        """
        params = []

        if category:
            base_query += " AND category = ?"
            params.append(category)

        base_query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cur.execute(base_query, tuple(params))
    
    rows = cur.fetchall()
    conn.close()
    return rows

def get_news_by_id(news_id: int):
    """
    Վերադարձնում է մեկ նորություն ըստ ID‑ի։
    """
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            SELECT * FROM news 
            WHERE id = %s AND published = TRUE
            """,
            (news_id,),
        )
    else:
        cur.execute(
            "SELECT * FROM news WHERE id = ? AND published = 1",
            (news_id,),
        )
    
    row = cur.fetchone()
    conn.close()
    return row

# ------------ Listings helpers ------------

def save_listing(category: str, chat_id: int, thread_id: int | None,
                 user_id: int, message_id: int, text: str) -> int:
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO listings (category, chat_id, thread_id, user_id, message_id, text)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (category, str(chat_id), str(thread_id) if thread_id is not None else None,
             str(user_id), str(message_id), text),
        )
        listing_id = cur.fetchone()['id']
    else:
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
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            DELETE FROM listings
            WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '%s days'
            """,
            (days,),
        )
    else:
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
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM listings
            WHERE user_id = %s
              AND created_at >= CURRENT_TIMESTAMP - INTERVAL '%s days'
              AND text = %s
            """,
            (str(user_id), days, text),
        )
    else:
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
    conn = get_connection()
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO violations (user_id, chat_id, vtype)
            VALUES (%s, %s, %s)
            """,
            (str(user_id), str(chat_id), vtype),
        )
    else:
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
    cur = get_cursor(conn)
    
    if DATABASE_URL:
        cur.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM violations
            WHERE user_id = %s
              AND chat_id = %s
              AND vtype = %s
              AND created_at >= CURRENT_TIMESTAMP - INTERVAL '%s hours'
            """,
            (str(user_id), str(chat_id), vtype, within_hours),
        )
    else:
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

def delete_old_news(days: int = 30) -> int:  # 365 → 30
    """
    Delete news older than X days (30 days default).
    """
    conn = get_connection()
    cur = get_cursor(conn)
    
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        
        if DATABASE_URL:
            cur.execute(
                "DELETE FROM news WHERE created_at < %s AND published = TRUE",
                (cutoff_date,)
            )
        else:
            cur.execute(
                "DELETE FROM news WHERE datetime(created_at) < datetime(?) AND published = 1",
                (cutoff_date,)
            )
        
        deleted_count = cur.rowcount
        conn.commit()
        logger.info(f"🧹 Deleted {deleted_count} news older than {days} days")
        return deleted_count
        
    except Exception as e:
        logger.error(f"❌ Cleanup error: {e}")
        conn.rollback()
        return 0
    finally:
        cur.close()
        conn.close()


