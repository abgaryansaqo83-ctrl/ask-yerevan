import datetime
from typing import Literal
import random

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


CATEGORY_LABELS_HY: dict[EventCategory, str] = {
    "premiere": "Պրեմիերա",
    "film": "Ֆիլմ",
    "theatre": "Թատրոն",
    "opera": "Օպերա",
    "party": "Փարթի",
    "standup": "Ստենդ-ափ",
    "festival": "Փառատոն",
}


# ================== CATEGORY-BASED (menu buttons, LIVE) ==================


async def get_events_by_category(
    category: EventCategory,
    limit: int = 3,
) -> str:
    """
    Օգտագործվում է /news մենյուի / «Միջոցառումներ» կոճակների time-ում.
    LIVE ռեժիմով քաշում է event-ներ անմիջապես Tomsarkgh-ից,
    առանց DB-ի:
      - film  -> cinema category
      - theatre / opera / party / standup / festival -> իրենց բաժինները
    Ֆիքս առավոտվա scheduler-ներ այստեղ այլևս չկան,
    դրանք անցել են DB-ով աշխատող առանձին jobs-ի մեջ։
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
        # premiere-ը հիմա fixed բլոկ է DB logic-ում, այստեղ live չգործարկենք
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
