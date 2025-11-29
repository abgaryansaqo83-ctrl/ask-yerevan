# backend/armenia/events.py

import datetime
from typing import Literal

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
    limit: int = 3,
) -> str:
    """
    Օգտագործվելու է /news մենյուի time-ում.
    Տրված category-ով բերում է մինչև 3 տարբերակ (mock).
    """
    label = CATEGORY_LABELS_HY.get(category, "Իրադարձություններ")

    mock_events: list[dict] = []

    if category == "premiere":
        mock_events = [
            {
                "title": "Պրեմիերա. «Տարվա երգ 2025»",
                "venue": "Կ.Դեմիրճյանի անվ. Մարզահամերգային համալիր",
                "time": "Շաբաթ, 20:00",
                "price": "6000–38000",
            },
        ]
    elif category == "film":
        mock_events = [
            {
                "title": "Ֆիլմ. «Երևանյան գիշերներ»",
                "venue": "Մոսկվա կինոթատրոն",
                "time": "Այսօր՝ 19:30",
                "price": "3000–7000",
            },
            {
                "title": "Ֆիլմ. «Քայլ դեպի արևը»",
                "venue": "Կինոպարկ Երևան Մոլ",
                "time": "Այսօր՝ 21:00",
                "price": "3500–8000",
            },
        ]
    elif category == "theatre":
        mock_events = [
            {
                "title": "«Ազիզյանները թատրոնում»",
                "venue": "Գ.Սունդուկյանի անվ. ազգային ակադ. թատրոն",
                "time": "Այսօր՝ 19:00",
                "price": "3500–12000",
            },
            {
                "title": "«Իմ կնոջ ամուսինը»",
                "venue": "Հ.Պարոնյանի անվ. երաժշտական կոմեդիայի թատրոն",
                "time": "Այսօր՝ 20:00",
                "price": "3000–12000",
            },
        ]
    elif category == "opera":
        mock_events = [
            {
                "title": "Պ.Չայկովսկի «Կարապի լիճը»",
                "venue": "Ա.Սպենդիարյանի անվ. օպերայի և բալետի թատրոն",
                "time": "Վաղը՝ 19:00",
                "price": "5000–28000",
            },
        ]
    elif category == "party":
        mock_events = [
            {
                "title": "Party. «Հայ Եռալեգենդ» երեկո",
                "venue": "Երևան, event hall",
                "time": "Շաբաթ՝ 21:00",
                "price": "6000–13500",
            },
        ]
    elif category == "standup":
        mock_events = [
            {
                "title": "HD Stand Up Live",
                "venue": "Retro Stand Up club",
                "time": "Կիրակի՝ 20:00",
                "price": "4000–8000",
            },
        ]

    if not mock_events:
        return (
            f"😕 Այս պահին {label.lower()} ուղղությամբ միջոցառումներ չեն գտնվել։\n"
            f"{_footer_source()}"
        )

    lines = [f"🎭 {label} — {len(mock_events)} տարբերակ\n"]
    for ev in mock_events[:limit]:
        lines.append(
            _format_event_line(
                ev["title"],
                ev["venue"],
                ev["time"],
                ev["price"],
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
