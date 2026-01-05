import datetime
from typing import Literal
import random

from backend.database import get_all_news
from backend.armenia.events_sources import fetch_live_events_for_category

EventCategory = Literal[
    "premiere",  # պրեմիերա (այժմ չի օգտագործվում LIVE՝ մենյուի համար)
    "film",      # ֆիլմ
    "theatre",   # թատրոն
    "opera",     # օպերա
    "party",     # փարթի
    "standup",   # ստենդ-ափ
    "festival",  # փառատոն
]

# ================== HELPERS ==================

def _format_event_line(title: str, place: str, time_str: str, price: str) -> str:
    if len(price) > 80:
        price = price[:77] + "..."
    return (
        f"🎫 {title}\n"
        f"📍 {place}\n"
        f"🕒 {time_str}\n"
        f"💸 {price}\n"
    )


CATEGORY_LABELS_HY: dict[EventCategory, str] = {
    "premiere": "Պրեմիերա",
    "film": "Ֆիլմ",
    "theatre": "Թատրոն",
    "opera": "Օպերա",
    "party": "Փարթի",
    "standup": "Ստենդ-ափ",
    "festival": "Փառատոն",
}

# ================== CATEGORY-BASED (menu buttons) ==================

async def get_events_by_category(
    category: str,
    limit: int = 3,
) -> str:
    """
    /menu կոճակների համար event-ներ է բերում.
    1) Նախ փորձում է գտնել AskYerevan news աղյուսակից (DB-first)
    2) Եթե DB-ում ոչինչ չկա, fallback է անում LIVE Tomsarkgh scraper-ին
    """
    # Մարդկային label-ներ header-ի համար
    label_map = {
        "film": "Կինո",
        "theatre": "Թատրոն",
        "pub": "Փաբ / ռեստորան",
        "standup": "Stand‑up",
        "events": "Միջոցառումներ",
    }
    label = label_map.get(category, "Իրադարձություններ")

    # ---------- 1) Փորձ DB-ից (news աղյուսակ) ----------
    today = datetime.date.today().isoformat()

    def _build_db_filter(category_key: str) -> dict:
        if category_key == "film":
            return {
                "categories": ["culture", "events"],
                "keywords": ["կինո", "film", "cinema", "movie"],
            }
        if category_key == "theatre":
            return {
                "categories": ["culture"],
                "keywords": ["թատրոն", "theatre", "performance", "պիես"],
            }
        if category_key == "standup":
            return {
                "categories": ["events"],
                "keywords": ["stand-up", "stand up", "ստենդ-ափ", "ստենդափ"],
            }
        if category_key == "pub":
            return {
                "categories": ["events", "city"],
                "keywords": ["փաբ", "pub", "club", "bar", "ակումբ", "nightlife"],
            }
        if category_key == "events":
            return {
                "categories": ["events", "holiday_events", "city", "culture"],
                "keywords": [],
            }
        return {
            "categories": ["events", "culture", "city", "holiday_events"],
            "keywords": [],
        }

    cfg = _build_db_filter(category)

    rows = []
    for cat in cfg["categories"]:
        rows_cat = get_all_news(limit=50, category=cat)
        rows.extend(rows_cat)

    def _row_is_future(row: dict) -> bool:
        d = row.get("eventdate")
        if not d:
            return False
        try:
            return d >= today
        except Exception:
            return False

    future_rows = [r for r in rows if _row_is_future(r)]

    keywords = cfg["keywords"]

    def _row_matches_keywords(row: dict) -> bool:
        if not keywords:
            return True
        text = (row.get("title_hy") or "") + " " + (row.get("content_hy") or "")
        text_low = text.lower()
        return any(k.lower() in text_low for k in keywords)

    filtered = [r for r in future_rows if _row_matches_keywords(r)]

    if filtered:
        def _sort_key(row: dict):
            d = row.get("eventdate") or ""
            t = row.get("eventtime") or ""
            return (d, t)

        filtered.sort(key=_sort_key)

        k = min(limit, len(filtered))
        chosen = random.sample(filtered, k=k)

        header = f"🎭 {label} — {k} տարբերակ (AskYerevan կայքից)\n\n"

        lines: list[str] = []
        for row in chosen:
            title = row.get("title_hy") or "Անվերնագիր միջոցառում"
            venue = row.get("venue_hy") or "Վայր նշված չէ"
            date_str = row.get("eventdate") or ""
            time_str = row.get("eventtime") or ""
            nice_time = f"{date_str} {time_str}".strip()
            price = row.get("price_hy") or "գինը նշված չէ"

            lines.append(_format_event_line(title, venue, nice_time, price))

        more_link_map = {
            "film": "/hy/news?category=culture",
            "theatre": "/hy/news?category=culture",
            "standup": "/hy/news?category=events",
            "pub": "/hy/news?category=events",
            "events": "/hy/news?category=events",
        }
        more_url = more_link_map.get(category, "/hy/news")
        lines.append(
            f"🔗 Ավելին AskYerevan կայքում՝ https://ask-yerevan.onrender.com{more_url}"
        )

        return header + "\n".join(lines)

    # ---------- 2) Fallback → LIVE Tomsarkgh ----------
    live_category_map = {
        "film": "cinema",
        "theatre": "theatre",
        "pub": "party",
        "standup": "festival",
        "events": "festival",
    }
    kind = live_category_map.get(category)
    if kind is None:
        return f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։"

    events = fetch_live_events_for_category(kind, limit=20)

    if not events:
        return f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։"

    today_date = datetime.date.today()
    future_events: list[dict] = []
    for ev in events:
        try:
            d = datetime.date.fromisoformat(ev.get("date", ""))
        except Exception:
            continue
        if d >= today_date:
            future_events.append(ev)

    if future_events:
        source_list = future_events
        day_label = "մոտակա օրերից"
    else:
        source_list = events
        day_label = "վերջին միջոցառումներից"

    k = min(limit, len(source_list))
    chosen = random.sample(source_list, k=k)

    header = f"🎭 {label} — {k} տարբերակ ({day_label}, LIVE)\n\n"

    lines = []
    for ev in chosen:
        title = ev.get("title") or "Անվերնագիր միջոցառում"
        venue = ev.get("place") or "Վայր նշված չէ"
        date_str = ev.get("date") or ""
        time_str = ev.get("time") or ""
        nice_time = f"{date_str} {time_str}".strip()
        price = ev.get("price") or "գինը նշված չէ"

        lines.append(_format_event_line(title, venue, nice_time, price))

    lines.append(
        "🔗 Ավելին AskYerevan կայքում՝ https://ask-yerevan.onrender.com/hy/news"
    )

    return header + "\n".join(lines)
