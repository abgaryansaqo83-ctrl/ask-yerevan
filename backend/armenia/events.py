# backend/armenia/events.py

import datetime
from typing import Literal
import random

from .events_sources import (
    fetch_cinema_from_tomsarkgh,
    fetch_theatre_from_tomsarkgh,
    fetch_opera_from_tomsarkgh,
)
from backend.armenia.events_sources import fetch_live_events_for_category

EventCategory = Literal[
    "premiere",  # պրեմիերա
    "film",      # ֆիլմ
    "theatre",   # թատրոն
    "opera",     # օպերա
    "party",     # փարթի
    "standup",   # ստենդ-ափ
    "festival",  # փառատոն
]

# ================== HELPERS ==================

def _format_event_line(title: str, place: str, time_str: str, price: str) -> str:
    """
    Մեկ իրադարձության տողի ֆորմատ.
    🎫 Վերնագիր
    📍 Վայր
    🕒 Ժամ կամ օր
    💸 Գին
    """
    return (
        f"🎫 {title}\n"
        f"📍 {place}\n"
        f"🕒 {time_str}\n"
        f"💸 {price}\n"
    )


def _footer_source() -> str:
    """
    Աղբյուրի հիշատակումն այժմ անջատված է։
    Թողնում ենք ֆունկցիան, որ եթե պետք լինի՝ հետո հեշտ միացնենք։
    """
    return ""


def _pick_events_for_range(
    rows: list[dict],
    today: datetime.date,
    limit: int,
) -> tuple[list[dict], str]:
    """
    Ընտրում է մինչև `limit` event այս կամ մոտակա օրերից.
    - Սկզբում փորձում է բրել հենց այսօրվա event-ները
    - Եթե այսօր չկան, վերցնում է ամենամոտ ապագա օրվա event-ները
    Վերադարձնում է (events, human_readable_day_label)
    """
    if not rows:
        return [], ""

    # rows պահում ենք as-is, date-ը ISO string է
    # 1) այսօր
    today_iso = today.isoformat()
    todays = [r for r in rows if r.get("date") == today_iso]

    if todays:
        chosen_source = todays
        day_label = "այսօր"
    else:
        # 2) եթե այսօր չկա, գտնել ամենամոտ ապագա օրերը
        future = []
        for r in rows:
            try:
                d = datetime.date.fromisoformat(r.get("date", ""))
            except Exception:
                continue
            if d >= today:
                future.append((d, r))

        if not future:
            return [], ""

        # sort by date, pick the nearest date
        future.sort(key=lambda x: x[0])
        nearest_date = future[0][0]
        nearest_iso = nearest_date.isoformat()
        nearest_rows = [r for (d, r) in future if d == nearest_date]

        chosen_source = nearest_rows
        # Label՝ օրինակ "մոտակա օրերից (Դեկտեմբեր 7, Շաբաթ)"
        day_label = nearest_date.strftime("մոտակա օրերից (%d %B, %A)")

    k = min(limit, len(chosen_source))
    chosen = random.sample(chosen_source, k=k)
    return chosen, day_label


# ================== WEEK PREMIERE ==================


async def get_week_premiere() -> str:
    """
    Երկուշաբթի 08:30 – «Շաբաթվա պրեմիերա».
    Փորձում է գտնել առաջիկա օրերի կինո/թատրոն/օպերա live event-ներից մեկը.
    Եթե չի ստացվում, վերադարձնում է info-տեքստ, որ այս շաբաթ պրեմիերա չի գտնվել։
    """
    today = datetime.date.today()
    week_label = today.isocalendar().week

    # 1) Քաշում ենք live event-ները (sync scraper-ներ են, կարող են մի քիչ դանդաղ լինել)
    cinema = fetch_cinema_from_tomsarkgh(limit=20)
    theatre = fetch_theatre_from_tomsarkgh(limit=20)
    opera = fetch_opera_from_tomsarkgh(limit=20)

    all_events = cinema + theatre + opera
    if not all_events:
        return f"✨ Շաբաթվա պրեմիերա #{week_label}\n\nԱյս շաբաթ նոր պրեմիերա չեմ գտել 🙂"

    # 2) Sort by ближайшая дата/ժամ
    def _dt_key(ev: dict):
        d = ev.get("date") or ""
        t = ev.get("time") or ""
        try:
            if t:
                return datetime.datetime.fromisoformat(f"{d} {t}")
            return datetime.datetime.fromisoformat(d)
        except Exception:
            return datetime.datetime.max

    all_events.sort(key=_dt_key)

    # 3) Վերցնենք ամենամոտիկը (կամ random առաջին մի քանիից)
    candidates = all_events[:5]
    ev = random.choice(candidates)

    title = ev["title"]
    venue = ev["place"]
    date_str = ev.get("date") or ""
    time_str = ev.get("time") or ""
    nice_time = f"{date_str} • 🕒 {time_str}" if time_str else date_str or "ժամը նշված չէ"

    header = f"✨ Շաբաթվա պրեմիերա #{week_label}\n\n"
    body = _format_event_line(title, venue, nice_time, "գինը նշված չէ")

    return header + body


# ================== NEXT DAY EVENTS ==================


async def get_next_day_films_and_plays(
    target_date: datetime.date | None = None,
) -> list[str]:
    """
    Չորեքշաբթիից կիրակի, ամեն օր 09:00.
    Հաջորդ օրվա 3 ֆիլմ + 2 ներկայացում, առանձին հաղորդագրություններով (LIVE, Tomsarkgh).
    """
    if target_date is None:
        target_date = datetime.date.today() + datetime.timedelta(days=1)

    target_iso = target_date.isoformat()
    weekday_label = target_date.strftime("%d %B, %A")

    # Քաշում ենք live կինո/թատրոն event-ները Tomsarkgh-ից
    all_cinema = fetch_live_events_for_category("cinema", limit=50)
    all_theatre = fetch_live_events_for_category("theatre", limit=50)

    # Թողնենք միայն այն event-ները, որոնք հենց target օրվա համար են
    films_rows = [ev for ev in all_cinema if ev.get("date") == target_iso]
    plays_rows = [ev for ev in all_theatre if ev.get("date") == target_iso]

    # Վերցնենք մինչև 3 ֆիլմ 2 ներկայացում random
    
    films = random.sample(films_rows, k=min(3, len(films_rows)))
    plays = random.sample(plays_rows, k=min(2, len(plays_rows)))


    if not films and not plays:
        return [
            f"📅 {weekday_label}\n\n"
            "Այս պահին վաղվա համար կինո կամ թատրոնի ծրագրեր չեն գտնվել։"
        ]

    messages: list[str] = []

    for ev in films + plays:
        header = f"📅 {weekday_label}\n\n"
        title = ev["title"]
        venue = ev.get("place") or "Վայր նշված չէ"
        time_str = ev.get("time") or "ժամը նշված չէ"
        price = ev.get("price") or "գինը նշված չէ"

        body = _format_event_line(title, venue, time_str, price)
        messages.append(header + body)

    return messages


# ================== CATEGORY-BASED (news menu) ==================


CATEGORY_LABELS_HY: dict[EventCategory, str] = {
    "premiere": "Պրեմիերա",
    "film": "Ֆիլմ",
    "theatre": "Թատրոն",
    "opera": "Օպերա",
    "party": "Փարթի",
    "standup": "Ստենդ-ափ",
    "festival": "Փառատոն",
}


async def get_events_by_category(
    category: EventCategory,
    limit: int = 5,
) -> str:
    """
    Օգտագործվում է /news մենյուի time-ում.
    LIVE ռեժիմով քաշում է event-ներ անմիջապես Tomsarkgh-ից,
    առանց DB-ի:
      - film  -> cinema category
      - theatre / opera / party / standup / festival -> իրենց բաժինները
    """
    label = CATEGORY_LABELS_HY.get(category, "Իրադարձություններ")

    # map /news կոճակների դեպի Tomsarkgh բաժինները
    live_category_map = {
        "film": "cinema",
        "theatre": "theatre",
        "opera": "opera",
        "party": "party",
        "standup": "party",      # stand-up-ը քաշում ենք party բաժնից
        "festival": "festival",
        # premiere-ը հիմա առանձին fixed բլոկ է, live-ով չենք քաշում
    }

    kind = live_category_map.get(category)
    if kind is None:
        return f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։"

    # LIVE events from Tomsarkgh
    events = fetch_live_events_for_category(kind, limit=20)

    if not events:
        return f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։"

    # Թողնում ենք միայն այսօրից սկսած event-ները, եթե հնարավոր է
    today = datetime.date.today()
    future_events: list[dict] = []
    for ev in events:
        try:
            d = datetime.date.fromisoformat(ev.get("date", ""))
        except Exception:
            continue
        if d >= today:
            future_events.append(ev)

    if future_events:
        source_list = future_events
        day_label = "մոտակա օրերից"
    else:
        # եթե ոչինչ չգտնվեց >= today, fallback՝ վերցնել ամբողջ events list-ը
        source_list = events
        day_label = "վերջին միջոցառումներից"

    k = min(limit, len(source_list))
    chosen = random.sample(source_list, k=k)

    header = f"🎭 {label} — {k} տարբերակ ({day_label})\n\n"

    lines: list[str] = []
    for ev in chosen:
        title = ev["title"]
        venue = ev.get("place") or "Վայր նշված չէ"
        date_str = ev.get("date") or ""
        time_str = ev.get("time") or ""
        nice_time = f"{date_str} {time_str}".strip()
        price = ev.get("price") or "գինը նշված չէ"

        lines.append(_format_event_line(title, venue, nice_time, price))

    return header + "\n".join(lines)


# ================== FESTIVAL EVENTS (7 days) ==================


async def get_festival_events_7days() -> str:
    """
    Եթե կան փառատոններ, չորեքշաբթի օրը հրապարակվող
    մոտակա 7 օրվա բոլոր միջոցառումները տվյալ փառատոնի շուրջ։ (mock)
    """
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=7)

    festival_name = "«Yerevan Jazz Festival»"
    events = [
        {
            "title": "Օպենինգ համերգ",
            "venue": "Կ.Դեմիրճյանի անվ. Մարզահամերգային համալիր",
            "time": f"{today.strftime('%d %B')} — 20:00",
            "price": "8000–30000",
        },
        {
            "title": "Jam Session Night",
            "venue": "Քաղաքի ջազ ակումբ",
            "time": f"{(today + datetime.timedelta(days=2)).strftime('%d %B')} — 21:00",
            "price": "5000–12000",
        },
    ]

    header = (
        f"🎉 Փառատոնային շաբաթ՝ {festival_name}\n"
        f"📅 {today.strftime('%d %B')} — {end_date.strftime('%d %B')}\n\n"
    )

    body_parts: list[str] = []
    for ev in events:
        body_parts.append(
            _format_event_line(
                ev["title"],
                ev["venue"],
                ev["time"],
                ev["price"],
            )
        )

    return header + "\n".join(body_parts)  # footer հանված է
