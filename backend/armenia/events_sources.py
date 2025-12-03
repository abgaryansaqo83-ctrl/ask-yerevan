# backend/armenia/events_sources.py

from datetime import date
from typing import List, Dict, Any

from backend.database import save_event, cleanup_old_events, get_today_events


# ---------- Dummy cinema events (test phase) ----------

def get_dummy_film_events() -> List[Dict[str, Any]]:
    today = date.today()
    return [
        {
            "title": "Կինոերեկո «Երևան by Night»",
            "date": today.isoformat(),
            "time": "19:30",
            "place": "Մոսկվա կինոթատրոն",
            "city": "Yerevan",
            "category": "cinema",
            "url": "https://example.com/event/yerevan-by-night",
            "source": "dummy",
        },
        {
            "title": "Արտհաուս ֆիլմերի մարաթոն",
            "date": today.isoformat(),
            "time": "20:00",
            "place": "Կինոակումբ «Հին Երևան»",
            "city": "Yerevan",
            "category": "cinema",
            "url": "https://example.com/event/arthouse-marathon",
            "source": "dummy",
        },
    ]


# ---------- Գիշերային refresh բոլոր ուղղությունների համար ----------

async def refresh_today_events():
    """
    Գիշերային job.
    - Մաքրում է հին event-ները.
    - Ջնջում է ներկա օրվա event-ները (որ կրկնություն չլինի).
    - Լցնում է այսօրվա նոր event-ները տարբեր կատեգորիաներով։
    Հիմա իրականում dummy-ով լցնում ենք միայն 'cinema'-ն։
    """

    # 1) ջնջել հին (օր. 30 օրից հին) event-ները
    cleanup_old_events(days=30)

    # 2) ջնջել այսօր գրանցված event-ները, որ սեղմ refresh լինի
    today = date.today().isoformat()
    _delete_today_events(today)

    # 3) Լցնել այսօրվա data-ն ըստ ուղղությունների
    # 3.1 Կինո (dummy, մինչ scrapers-ը գրենք)
    for ev in get_dummy_film_events():
        save_event(ev)

    # 3.2 Թատրոն / օպերա / փաբ / event-ներ
    # Հիմա դեռ ոչինչ չենք լցնում, հետո այստեղ կկանչենք իրական source fetch-եր
    # օրինակ.
    # for ev in await fetch_cinema_from_tomsarkgh():
    #     save_event(ev)
    # for ev in await fetch_theatre_from_tomsarkgh():
    #     save_event(ev)
    # ...


def _delete_today_events(today_iso: str) -> None:
    """
    Ջնջում է events table-ից տվյալ օրվա բոլոր գրառումները
    (քանի որ refresh_today_events-ը օրվա ամբողջ data-ն նորից է լցնելու)։
    """
    from backend.database import get_connection  # local import to avoid cycles

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE date = ?", (today_iso,))
    conn.commit()
    conn.close()


# ---------- Օգտագործվող helpers /news-ի համար ----------

def get_today_events_by_category(category: str, city: str = "Yerevan"):
    """
    Վերադարձնում է տվյալ օրվա event-ները ըստ category-ի (cinema/theatre/party/...). 
    """
    rows = get_today_events(city=city, category=category)
    return rows
