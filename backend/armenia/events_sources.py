# backend/armenia/events_sources.py

from datetime import date, timedelta


def get_dummy_film_events():
    """
    Ժամանակավոր test event-ներ, մինչև իրական կայքերից տվյալ քաշելը։
    Վերադարձնում է list[dict].
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
