# backend/armenia/events.py

import datetime
from typing import Literal
import random
from backend.armenia.events_sources import get_today_events_by_category


EventCategory = Literal[
    "premiere",  # պրեմիերա
    "film",      # ֆիլմ
    "theatre",   # թատրոն
    "opera",     # օպերա
    "party",     # փարթի
    "standup",   # ստենդ-ափ
    "festival",  # փառատոն
]

TOMSARKGH_URL = "https://www.tomsarkgh.am"


# ================== HELPERS ==================


def _format_event_line(title: str, place: str, time_str: str, price: str) -> str:
    """
    Մեկ իրադարձության տողի ֆորմատ.
    🎫 Վերնագիր
    📍 Վայր
    🕒 Ժամ
    💸 Գին
    """
    return (
        f"🎫 {title}\n"
        f"📍 {place}\n"
        f"🕒 {time_str}\n"
        f"💸 {price}\n"
    )


def _footer_source() -> str:
    """Աղբյուրի կարճ հիշատակում."""
    return f"\n🔎 Լրիվ ցանկը՝ {TOMSARKGH_URL}"


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

    return header + body + _footer_source()


# ================== NEXT DAY EVENTS ==================


async def get_next_day_films_and_plays(
    target_date: datetime.date | None = None,
) -> list[str]:
    """
    Չորեքշաբթիից կիրակի, ամեն օր 09:00.
    Հաջորդ օրվա 2 ֆիլմ + 2–3 ներկայացում, առանձին հաղորդագրություններով։
    """
    if target_date is None:
        target_date = datetime.date.today() + datetime.timedelta(days=1)

    weekday_label = target_date.strftime("%d %B, %A")

    # MOCK տվյալներ
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
        messages.append(header + body + _footer_source())

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
    Տրված category-ով բերում է մինչև `limit` տարբերակ՝ DB-ից,
    random ձևով ընտրված տվյալ օրվա event-ներից։
    """
    label = CATEGORY_LABELS_HY.get(category, "Իրադարձություններ")

    # category map DB-ի համար
    db_category_map = {
        "film": "cinema",
        "theatre": "theatre",
        "opera": "opera",
        "party": "party",
        "standup": "party",      # օրինակ՝ standup-ը նույն party category-ում
        "festival": "festival",
        "premiere": "cinema",    # կամ ինչով որ որոշես
    }

    db_cat = db_category_map.get(category)
    if db_cat is None:
        return (
            f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։\n"
            f"{_footer_source()}"
        )

    # Վերցնում ենք տվյալ օրվա event-ները տվյալ կատեգորիայից
    rows = get_today_events_by_category(db_cat)
    events = list(rows)

    if not events:
        return (
            f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։\n"
            f"{_footer_source()}"
        )

    k = min(limit, len(events))
    chosen = random.sample(events, k=k)

    lines: list[str] = [f"🎭 {label} — {k} տարբերակ\n"]
    for ev in chosen:
        title = ev["title"]
        venue = ev["place"]
        # date + time համադրում ենք
        date_str = ev["date"]
        time_str = ev.get("time") or ""
        nice_time = f"{date_str} {time_str}".strip()

        # գին հիմա չունենք DB-ում, placeholder
        price = "գինը նշված չէ"

        lines.append(
            _format_event_line(
                title,
                venue,
                nice_time,
                price,
            )
        )

    lines.append(_footer_source())
    return "\n".join(lines)


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

    return header + "\n".join(body_parts) + _footer_source()
