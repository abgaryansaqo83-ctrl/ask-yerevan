# backend/armenia/events_sources.py

from datetime import date, timedelta
from typing import List, Dict, Any

from backend.database import save_event, get_upcoming_events


# ---------- Dummy cinema events (test phase) ----------

def get_dummy_film_events() -> List[Dict[str, Any]]:
    """
    Ժամանակավոր test event-ներ, մինչև իրական կայքերից տվյալ քաշելը։
    Վերադարձնում է list[dict] նույն կառուցվածքով, ինչ events table-ը սպասում է։
    """
    today = date.today()
    return [
        {
            "title": "Կինոերեկո «Երևան by Night»",
            "date": (today + timedelta(days=1)).isoformat(),
            "time": "19:30",
            "place": "Մոսկվա կինոթատրոն",
            "city": "Yerevan",
            "category": "cinema",
            "url": "https://example.com/event/yerevan-by-night",
            "source": "dummy",
        },
        {
            "title": "Արտհաուս ֆիլմերի մարաթոն",
            "date": (today + timedelta(days=2)).isoformat(),
            "time": "20:00",
            "place": "Կինոակումբ «Հին Երևան»",
            "city": "Yerevan",
            "category": "cinema",
            "url": "https://example.com/event/arthouse-marathon",
            "source": "dummy",
        },
    ]


# ---------- High-level helpers, որ հետո կօգտագործի /news callback-ը ----------

def refresh_dummy_cinema_events(save_to_db: bool = True) -> List[Dict[str, Any]]:
    """
    Հիմա պարզապես վերադարձնում է dummy կինո event-ները և, ցանկության դեպքում,
    գրանցում դրանք events աղյուսակում future օգտագործման համար։
    Հետագայում այստեղ կդնենք իրական source fetch (tomsarkgh / ticket-am և այլն)։
    """
    events = get_dummy_film_events()

    if save_to_db:
        for ev in events:
            try:
                save_event(ev)
            except Exception:
                # Եթե միևնույն dummy-ն մի քանի անգամ փորձարկենք, errors-ից խուսափելու համար
                continue

    return events


def get_upcoming_cinema_events_from_db(limit: int = 10):
    """
    Օգնական՝ DB-ից վերցնելու մոտակա կինո event-ները Երևանի համար։
    Կօգտագործվի, երբ իրական աղբյուրներից սկսենք լցնել events աղյուսակը։
    """
    rows = get_upcoming_events(limit=limit, city="Yerevan", category="cinema")
    return rows
