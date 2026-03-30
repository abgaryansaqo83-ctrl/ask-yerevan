# backend/database.py

import os
import datetime
from pathlib import Path
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any, List
from typing import Iterable

from backend.utils.logger import logger

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL mode
    import psycopg2
    from psycopg2.extras import RealDictCursor

    def get_connection():
        """Return a PostgreSQL connection."""
        print(f"🐘 Using PostgreSQL: {DATABASE_URL[:30]}...")
        return psycopg2.connect(DATABASE_URL)

    def get_cursor(conn):
        """Return a dict cursor for PostgreSQL."""
        return conn.cursor(cursor_factory=RealDictCursor)

else:
    # SQLite fallback (local dev)
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
        """Return a cursor for SQLite."""
        return conn.cursor()


# ============================================================================
# INIT DB — CREATE TABLES
# ============================================================================

def init_db():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cur = get_cursor(conn)

    # Dialect helpers
    if DATABASE_URL:
        autoincrement = "SERIAL PRIMARY KEY"
        datetime_now = "CURRENT_TIMESTAMP"
        bool_type = "BOOLEAN"
    else:
        autoincrement = "INTEGER PRIMARY KEY AUTOINCREMENT"
        datetime_now = "datetime('now')"
        bool_type = "INTEGER"

    # EVENTS table (for Telegram schedule, Madrid, etc.)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS events (
            id {autoincrement},
            title      TEXT NOT NULL,
            date       TEXT,
            time       TEXT,
            place      TEXT,
            city       TEXT,
            category   TEXT,
            url        TEXT,
            source     TEXT,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)

    # USERS table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id         {autoincrement},
            chat_id    TEXT UNIQUE,
            username   TEXT,
            first_name TEXT,
            last_name  TEXT,
            language   TEXT,
            created_at TIMESTAMP
        )
    """)

    # VIOLATIONS table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS violations (
            id        {autoincrement},
            user_id   TEXT NOT NULL,
            chat_id   TEXT NOT NULL,
            vtype     TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)

    # NEWS table — MAIN AskYerevan events/news storage
    # Includes structured event fields for website + Telegram schedule
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS news (
            id          {autoincrement},
            title_hy    TEXT NOT NULL,
            title_en    TEXT NOT NULL,
            content_hy  TEXT NOT NULL,
            content_en  TEXT NOT NULL,
            image_url   TEXT,
            category    TEXT DEFAULT 'general',
            eventdate   TEXT,
            eventtime   TEXT,
            venue_hy    TEXT,
            price_hy    TEXT,
            source_url  TEXT UNIQUE,
            published   {bool_type} DEFAULT {'TRUE' if DATABASE_URL else 1},
            created_at  TIMESTAMP DEFAULT {datetime_now}
        )
    """)

    # MEMORY table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS memory (
            id         {autoincrement},
            chat_id    TEXT,
            key        TEXT,
            value      TEXT,
            updated_at TIMESTAMP
        )
    """)

    # LISTINGS table (user listings in Telegram group)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS listings (
            id         {autoincrement},
            category   TEXT NOT NULL,
            chat_id    TEXT NOT NULL,
            thread_id  TEXT,
            user_id    TEXT NOT NULL,
            message_id TEXT NOT NULL,
            text       TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT {datetime_now}
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")


# ============================================================================
# USER HELPERS
# ============================================================================

def save_user(chat_id: int,
              username: Optional[str] = None,
              first_name: Optional[str] = None,
              last_name: Optional[str] = None,
              language: str = "hy") -> None:
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO users (chat_id, username, first_name, last_name, language, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (chat_id) DO UPDATE SET
                username   = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name  = EXCLUDED.last_name,
                language   = EXCLUDED.language
            """,
            (chat_id, username, first_name, last_name, language),
        )
    else:
        cur.execute(
            """
            INSERT OR REPLACE INTO users (chat_id, username, first_name, last_name, language, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (chat_id, username, first_name, last_name, language),
        )

    conn.commit()
    conn.close()


def get_user(chat_id: int):
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute("SELECT * FROM users WHERE chat_id = %s", (str(chat_id),))
    else:
        cur.execute("SELECT * FROM users WHERE chat_id = ?", (str(chat_id),))

    row = cur.fetchone()
    conn.close()
    return row


# ============================================================================
# EVENTS HELPERS  (generic events table)
# ============================================================================

def save_event(event: Dict[str, Any]) -> Optional[int]:
    """
    Generic events table (can be used for Madrid or other sources).
    """
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
        event_id = result["id"] if result else None
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


def get_upcoming_events(limit: int = 20,
                        city: Optional[str] = None,
                        category: Optional[str] = None):
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        query = """
            SELECT * FROM events
            WHERE date IS NOT NULL
              AND date >= CURRENT_DATE
        """
    else:
        query = """
            SELECT * FROM events
            WHERE date IS NOT NULL
              AND datetime(date) >= date('now')
        """

    params: List[Any] = []

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
            "DELETE FROM events WHERE date < CURRENT_DATE - INTERVAL %s DAY",
            (days,),
        )
    else:
        cur.execute(
            "DELETE FROM events WHERE datetime(date) < datetime('now', ?)",
            (f"-{days} days",),
        )

    conn.commit()
    conn.close()


def get_today_events(city: Optional[str] = None,
                     category: Optional[str] = None):
    today = date.today().isoformat()
    conn = get_connection()
    cur = get_cursor(conn)

    query = "SELECT * FROM events WHERE date = " + ("%s" if DATABASE_URL else "?")
    params: List[Any] = [today]

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


# ============================================================================
# NEWS HELPERS  (AskYerevan events/news)
# ============================================================================

def save_news(
    title_hy: str,
    title_en: str,
    content_hy: str,
    content_en: str,
    image_url: Optional[str] = None,
    category: str = "general",
    source_url: Optional[str] = None,
    eventdate: Optional[str] = None,
    eventtime: Optional[str] = None,
    venue_hy: Optional[str] = None,
    price_hy: Optional[str] = None,
    image_2: Optional[str] = None,
    image_3: Optional[str] = None,
    video_url: Optional[str] = None,
) -> Optional[int]:
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO news (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                source_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_url) DO NOTHING
            """,
            (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                source_url,
            ),
        )
    else:
        cur.execute(
            """
            INSERT OR IGNORE INTO news (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                source_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                source_url,
            ),
        )

    conn.commit()
    if DATABASE_URL:
        cur.execute("SELECT lastval()")
        row = cur.fetchone()
        news_id = row[0] if row else None
    else:
        news_id = cur.lastrowid
    conn.close()
    return news_id

def get_all_news(limit: int = 10,
                 category: Optional[str] = None):
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        base_query = """
            SELECT * FROM news
            WHERE published = TRUE
        """
        params: List[Any] = []

        if category:
            base_query += " AND category = %s"
            params.append(category)

        # վերջին 6 ամիսը, բայց eventdate ունենալու դեպքում սրան կարող ենք վերադառնալ հետո
        base_query += " AND created_at >= NOW() - INTERVAL '6 months'"
        base_query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(base_query, tuple(params))
    else:
        base_query = """
            SELECT * FROM news
            WHERE published = 1
        """
        params: List[Any] = []

        if category:
            base_query += " AND category = ?"
            params.append(category)

        base_query += " AND created_at >= datetime('now', '-6 months')"
        base_query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cur.execute(base_query, tuple(params))

    rows = cur.fetchall()
    conn.close()
    return rows


def get_news_by_id(news_id: int):
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            "SELECT * FROM news WHERE id = %s AND published = TRUE",
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

def get_random_news_with_image(category: str):
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            SELECT id, image_url
            FROM news
            WHERE published = TRUE
              AND category = %s
              AND image_url IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (category,),
        )
    else:
        cur.execute(
            """
            SELECT id, image_url
            FROM news
            WHERE published = 1
              AND category = ?
              AND image_url IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (category,),
        )

    row = cur.fetchone()
    conn.close()
    return row

def update_news(
    news_id: int,
    title_hy: str,
    title_en: str,
    content_hy: str,
    content_en: str,
    image_url: Optional[str],
    category: str,
    eventdate: Optional[str] = None,
    eventtime: Optional[str] = None,
    venue_hy: Optional[str] = None,
    price_hy: Optional[str] = None,
    image_2: Optional[str] = None,
    image_3: Optional[str] = None,
    video_url: Optional[str] = None,
) -> bool:
    """Update existing news item by ID. Returns True if updated."""
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            UPDATE news SET
                title_hy   = %s,
                title_en   = %s,
                content_hy = %s,
                content_en = %s,
                image_url  = %s,
                image_2    = %s,
                image_3    = %s,
                video_url  = %s,
                category   = %s,
                eventdate  = %s,
                eventtime  = %s,
                venue_hy   = %s,
                price_hy   = %s
            WHERE id = %s
            """,
            (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                news_id,
            ),
        )
    else:
        cur.execute(
            """
            UPDATE news SET
                title_hy   = ?,
                title_en   = ?,
                content_hy = ?,
                content_en = ?,
                image_url  = ?,
                image_2    = ?,
                image_3    = ?,
                video_url  = ?,
                category   = ?,
                eventdate  = ?,
                eventtime  = ?,
                venue_hy   = ?,
                price_hy   = ?
            WHERE id = ?
            """,
            (
                title_hy, title_en,
                content_hy, content_en,
                image_url, image_2, image_3, video_url,
                category,
                eventdate, eventtime,
                venue_hy, price_hy,
                news_id,
            ),
        )

    updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    return updated
    

def get_upcoming_holiday_events(days_ahead: int = 14, limit: int = 10):
    """
    Վերադարձնում է մոտակա holiday_events կատեգորիայի իրադարձությունները
    eventdate-ի հիման վրա, հաջորդ `days_ahead` օրերի մեջ։
    """
    conn = get_connection()
    cur = get_cursor(conn)

    today = date.today()
    end_date = today + timedelta(days=days_ahead)

    if DATABASE_URL:
        cur.execute(
            """
            SELECT *
            FROM news
            WHERE category = %s
              AND eventdate IS NOT NULL
              AND eventdate >= %s
              AND eventdate <= %s
              AND published = TRUE
            ORDER BY eventdate, eventtime
            LIMIT %s
            """,
            ("holiday_events", today.isoformat(), end_date.isoformat(), limit),
        )
    else:
        cur.execute(
            """
            SELECT *
            FROM news
            WHERE category = ?
              AND eventdate IS NOT NULL
              AND eventdate >= ?
              AND eventdate <= ?
              AND published = 1
            ORDER BY eventdate, eventtime
            LIMIT ?
            """,
            ("holiday_events", today.isoformat(), end_date.isoformat(), limit),
        )

    rows = cur.fetchall()
    conn.close()
    return rows


def get_events_for_date(target_date: date,
                        max_per_category: int = 3):
    """
    Վերադարձնում է նշված օրվա event-ները news աղյուսակից՝
    ըստ category-ի սահմանափակումով:
    max_per_category – ամեն կատեգորիայից առավելագույն քանակը։
    """
    conn = get_connection()
    cur = get_cursor(conn)

    # պետական օրվա համար մեզ հետաքրքրում են այս կատեգորիաները
    categories = ["events", "culture", "city", "holiday_events"]

    results = []

    if DATABASE_URL:
        for cat in categories:
            cur.execute(
                """
                SELECT *
                FROM news
                WHERE eventdate = %s
                  AND category = %s
                  AND published = TRUE
                ORDER BY eventtime, created_at
                LIMIT %s
                """,
                (target_date.isoformat(), cat, max_per_category),
            )
            rows = cur.fetchall()
            results.extend(rows)
    else:
        for cat in categories:
            cur.execute(
                """
                SELECT *
                FROM news
                WHERE eventdate = ?
                  AND category = ?
                  AND published = 1
                ORDER BY eventtime, created_at
                LIMIT ?
                """,
                (target_date.isoformat(), cat, max_per_category),
            )
            rows = cur.fetchall()
            results.extend(rows)

    conn.close()
    return results


def delete_old_news(days: int = 90) -> int:
    """
    Delete news older than X days (90 days default).
    """
    conn = get_connection()
    cur = get_cursor(conn)

    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        if DATABASE_URL:
            cur.execute(
                "DELETE FROM news WHERE created_at < %s AND published = TRUE",
                (cutoff_date,),
            )
        else:
            cur.execute(
                "DELETE FROM news WHERE datetime(created_at) < datetime(?) AND published = 1",
                (cutoff_date,),
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


# ============================================================================
# QUESTIONS HELPERS  (unanswered group questions)
# ============================================================================

def save_question(chat_id: int, message_id: int, user_id: int, text: str) -> int:
    """
    Պահում ենք հարցը questions աղյուսակում, վերադարձնում ID-ն.
    Մշակված է PostgreSQL-ի համար (DATABASE_URL չկա SQLite-ում questions table).
    """
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(
        """
        INSERT INTO questions (chat_id, message_id, user_id, text)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (chat_id, message_id, user_id, text),
    )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row["id"]


def mark_question_answered(question_id: int) -> None:
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(
        "UPDATE questions SET answered = TRUE WHERE id = %s;",
        (question_id,),
    )
    conn.commit()
    conn.close()


def get_unanswered_questions_older_than(minutes: int) -> list[dict]:
    """
    Վերադարձնում է բոլոր հարցերը, որոնք դեռ answered = FALSE են
    և ստեղծվել են minutes րոպեից վաղ, + user-ի լեզուն users աղյուսակից։
    """
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        SELECT
          q.id,
          q.chat_id,
          q.message_id,
          q.user_id,
          q.text,
          q.created_at,
          u.language AS user_lang
        FROM questions q
        JOIN users u
          ON u.chat_id = q.user_id::text   -- եթե DATABASE_URL/Postgres
        WHERE q.answered = FALSE
          AND q.created_at <= NOW() - INTERVAL %s MINUTE
        ORDER BY q.created_at ASC;
        """,
        (minutes,),
    )

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================================
# LISTINGS HELPERS
# ============================================================================

def save_listing(category: str,
                 chat_id: int,
                 thread_id: Optional[int],
                 user_id: int,
                 message_id: int,
                 text: str) -> int:
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            INSERT INTO listings (category, chat_id, thread_id, user_id, message_id, text)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                category,
                str(chat_id),
                str(thread_id) if thread_id is not None else None,
                str(user_id),
                str(message_id),
                text,
            ),
        )
        listing_id = cur.fetchone()["id"]
    else:
        cur.execute(
            """
            INSERT INTO listings (category, chat_id, thread_id, user_id, message_id, text)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                category,
                str(chat_id),
                str(thread_id) if thread_id is not None else None,
                str(user_id),
                str(message_id),
                text,
            ),
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
            WHERE created_at < CURRENT_TIMESTAMP - INTERVAL %s DAY
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


def count_similar_listings(user_id: int,
                           text: str,
                           days: int = 15) -> int:
    conn = get_connection()
    cur = get_cursor(conn)

    if DATABASE_URL:
        cur.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM listings
            WHERE user_id = %s
              AND created_at >= CURRENT_TIMESTAMP - INTERVAL %s DAY
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


# ============================================================================
# VIOLATIONS HELPERS
# ============================================================================

def register_violation(user_id: int,
                       chat_id: int,
                       vtype: str) -> None:
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


def count_violations(user_id: int,
                     chat_id: int,
                     vtype: str,
                     within_hours: int) -> int:
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
              AND created_at >= CURRENT_TIMESTAMP - INTERVAL %s HOUR
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
            (str(user_id), str(chat_id), vtype, f"-{withinhours} hours"),
        )

    row = cur.fetchone()
    conn.close()
    return int(row["cnt"] if row else 0)

# ============================================================================
# PLACE LIKES / RATINGS / COMMENTS
# ============================================================================

# ── LIKES ────────────────────────────────────────────────────────────────────

def toggle_place_like(place_id: str, session_id: str) -> dict:
    """
    Like-ի toggle — եթե կա, հանում է, եթե չկա, ավելացնում է։
    Վերադարձնում է {"liked": bool, "count": int}
    """
    conn = get_connection()
    cur = get_cursor(conn)

    # ստուգում ա կա՞ արդեն
    cur.execute(
        "SELECT id FROM place_likes WHERE place_id = %s AND session_id = %s",
        (place_id, session_id),
    )
    existing = cur.fetchone()

    if existing:
        cur.execute(
            "DELETE FROM place_likes WHERE place_id = %s AND session_id = %s",
            (place_id, session_id),
        )
        liked = False
    else:
        cur.execute(
            "INSERT INTO place_likes (place_id, session_id) VALUES (%s, %s)",
            (place_id, session_id),
        )
        liked = True

    cur.execute(
        "SELECT COUNT(*) AS cnt FROM place_likes WHERE place_id = %s",
        (place_id,),
    )
    count = cur.fetchone()["cnt"]

    conn.commit()
    conn.close()
    return {"liked": liked, "count": int(count)}


def get_place_likes(place_id: str, session_id: str) -> dict:
    """Վերադարձնում է like-ի count + արդյոք session-ը like ա արել"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        "SELECT COUNT(*) AS cnt FROM place_likes WHERE place_id = %s",
        (place_id,),
    )
    count = cur.fetchone()["cnt"]

    cur.execute(
        "SELECT id FROM place_likes WHERE place_id = %s AND session_id = %s",
        (place_id, session_id),
    )
    liked = cur.fetchone() is not None

    conn.close()
    return {"liked": liked, "count": int(count)}


# ── RATINGS ───────────────────────────────────────────────────────────────────

def set_place_rating(place_id: str, session_id: str, rating: int) -> dict:
    """
    Session-ի rating-ը set կամ update անում է։
    Վերադարձնում է {"my_rating": int, "avg": float, "count": int}
    """
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        INSERT INTO place_ratings (place_id, session_id, rating)
        VALUES (%s, %s, %s)
        ON CONFLICT (place_id, session_id)
        DO UPDATE SET rating = EXCLUDED.rating
        """,
        (place_id, session_id, rating),
    )

    cur.execute(
        """
        SELECT COUNT(*) AS cnt, AVG(rating) AS avg
        FROM place_ratings WHERE place_id = %s
        """,
        (place_id,),
    )
    row = cur.fetchone()

    conn.commit()
    conn.close()
    return {
        "my_rating": rating,
        "avg": round(float(row["avg"]), 1) if row["avg"] else 0.0,
        "count": int(row["cnt"]),
    }


def get_place_rating(place_id: str, session_id: str) -> dict:
    """Վերադարձնում է avg rating + session-ի rating"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        SELECT COUNT(*) AS cnt, AVG(rating) AS avg
        FROM place_ratings WHERE place_id = %s
        """,
        (place_id,),
    )
    row = cur.fetchone()

    cur.execute(
        "SELECT rating FROM place_ratings WHERE place_id = %s AND session_id = %s",
        (place_id, session_id),
    )
    my = cur.fetchone()

    conn.close()
    return {
        "my_rating": int(my["rating"]) if my else 0,
        "avg": round(float(row["avg"]), 1) if row and row["avg"] else 0.0,
        "count": int(row["cnt"]) if row else 0,
    }


# ── COMMENTS ──────────────────────────────────────────────────────────────────

def add_place_comment(place_id: str, session_id: str, text: str, rating: int = 0) -> dict:
    """Comment ավելացնում է, վերադարձնում է id + created_at"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        INSERT INTO place_comments (place_id, session_id, text, rating)
        VALUES (%s, %s, %s, %s)
        RETURNING id, created_at
        """,
        (place_id, session_id, text[:500], rating or None),
    )
    row = cur.fetchone()

    conn.commit()
    conn.close()
    return {"id": row["id"], "created_at": str(row["created_at"])}


def get_place_comments(place_id: str) -> list:
    """Վերադարձնում է place-ի բոլոր comment-ները՝ նորից հին"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        SELECT id, text, rating, created_at
        FROM place_comments
        WHERE place_id = %s
        ORDER BY created_at DESC
        """,
        (place_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_place_comment_count(place_id: str) -> int:
    """Վերադարձնում է comment-ների քանակը"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        "SELECT COUNT(*) AS cnt FROM place_comments WHERE place_id = %s",
        (place_id,),
    )
    row = cur.fetchone()
    conn.close()
    return int(row["cnt"]) if row else 0

