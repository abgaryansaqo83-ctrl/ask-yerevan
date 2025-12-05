# backend/armenia/events.py

import datetime
from typing import Literal
import random
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
    Երկուշաբթի առավոտվա 08:30 հրապարակում.
    «Շաբաթվա պրեմիերա» ֆիլմ կամ ներկայացում՝ 1 հատ։ (mock)
    """
    today = datetime.date.today()
    week_label = today.isocalendar().week

    title = "Շաբաթվա պրեմիերա. «Կարապի լիճը»"
    venue = "Ա.Սպենդիարյանի անվան օպերայի և բալետի թատրոն"
    time = "Այս շաբաթ՝ 19:00"
    price = "5000–25000"

    header = f"✨ Շաբաթվա պրեմիերա #{week_label}\n\n"
    body = _format_event_line(title, venue, time, price)

    return header + body  # footer հանված է


# ================== NEXT DAY EVENTS ==================


async def get_next_day_films_and_plays(
    target_date: datetime.date | None = None,
) -> list[str]:
    """
    Չորեքշաբթիից կիրակի, ամեն օր 09:00.
    Հաջորդ օրվա 2 ֆիլմ + 2–3 ներկայացում, առանձին հաղորդագրություններով (mock).
    """
    if target_date is None:
        target_date = datetime.date.today() + datetime.timedelta(days=1)

    weekday_label = target_date.strftime("%d %B, %A")

    # MOCK տվյալներ (մինչև DB‑ով կապենք)
    films = [
        {
            "title": "Ֆիլմ. «Երևանյան գիշերներ»",
            "venue": "Մոսկվա կինոթատրոն",
            "time": "19:30",
            "price": "3000–7000",
        },
        {
            "title": "Ֆիլմ. «Քայլ դեպի արևը»",
            "venue": "Կինոպարկ Երևան Մոլ",
            "time": "21:00",
            "price": "3500–8000",
        },
    ]

    plays = [
        {
            "title": "Ներկայացում. «Իմ կնոջ ամուսինը»",
            "venue": "Հ.Պարոնյանի անվ. երաժշտական կոմեդիայի թատրոն",
            "time": "20:00",
            "price": "3000–12000",
        },
        {
            "title": "Ներկայացում. «Մեծ լռություն»",
            "venue": "Հ.Ղափլանյանի անվ. դրամատիկական թատրոն",
            "time": "19:00",
            "price": "3000–4000",
        },
    ]

    messages: list[str] = []

    for ev in films + plays:
        header = f"📅 {weekday_label}\n\n"
        body = _format_event_line(
            ev["title"],
            ev["venue"],
            ev["time"],
            ev["price"],
        )
        messages.append(header + body)  # footer հանված է

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
        price = "գինը նշված չէ"

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
