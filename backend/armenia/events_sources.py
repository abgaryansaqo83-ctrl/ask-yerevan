# backend/armenia/events_sources.py

from datetime import date
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

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


# ---------- Real cinema fetcher from Tomsarkgh ----------

CINEMA_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D4%BF%D5%AB%D5%B6%D5%B8"


def _scrape_one_tomsarkgh_event(url: str) -> Dict[str, Any] | None:
    """
    Քաշում է մեկ Tomsarkgh event էջը և վերադառնում է event dict:
    Եթե status code != 200 կամ կառուցվածքը կոտրված է, վերադարձնում է None։
    """
    try:
        resp = requests.get(url, timeout=15)
    except Exception:
        return None

    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Վերնագիր
    title_tag = soup.select_one("h1.event-name")
    if not title_tag:
        return None
    title = title_tag.get_text(strip=True)

    # Սկզբի ամսաթիվ/ժամ
    start_meta = soup.select_one("meta[itemprop=startDate]")
    raw_dt = start_meta["content"].strip() if start_meta and start_meta.has_attr("content") else ""
    date_part, time_part = None, None
    if " " in raw_dt:
        date_part, time_part = raw_dt.split(" ", 1)
    else:
        date_part = raw_dt

    if not date_part:
        return None

    # Վայրը
    venue_span = soup.select_one("div.occurrence_venue span[itemprop=name]")
    place = venue_span.get_text(strip=True) if venue_span else "Unknown venue"

    return {
        "title": title,
        "date": date_part,
        "time": time_part,
        "place": place,
        "city": "Yerevan",
        "category": "cinema",
        "url": url,
        "source": "tomsarkgh",
    }


def fetch_cinema_from_tomsarkgh(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Բացում է կինոյի category էջը և հավաքում է առաջին `limit` ֆիլմերի event URL-ները,
    հետո յուրաքանչյուրի համար քաշում է event տվյալները։

    Վերադարձնում է events-ի list (dict-եր):
    """
    events: List[Dict[str, Any]] = []

    try:
        resp = requests.get(CINEMA_CATEGORY_URL, timeout=15)
    except Exception:
        return events

    if resp.status_code != 200:
        return events

    soup = BeautifulSoup(resp.text, "html.parser")

    # Կինոների list-ում event link-երը
    # Սելեկտորը պետք է մի քիչ ճկուն լինի, այնպես որ վերցնում ենք բոլոր href-երը, որոնք սկսվում են /hy/event/
    links = []
    for a in soup.select('a[href^="/hy/event/"]'):
        href = a.get("href")
        if not href:
            continue
        full_url = "https://www.tomsarkgh.am" + href
        # Նույն event-ը մի քանի անգամ չավելացնելու համար
        if full_url not in links:
            links.append(full_url)
        if len(links) >= limit:
            break

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            events.append(ev)

    return events


# ---------- Գիշերային refresh բոլոր ուղղությունների համար ----------

async def refresh_today_events():
    """
    Գիշերային job.
    - Մաքրում է հին event-ները.
    - Ջնջում է ներկա օրվա event-ները (որ կրկնություն չլինի).
    - Լցնում է այսօրվա նոր event-ները տարբեր կատեգորիաներով։
    Հիմա իրականում dummy-ով և tomsarkgh-ով լցնում ենք 'cinema'-ն։
    """

    # 1) ջնջել հին (օր. 30 օրից հին) event-ները
    cleanup_old_events(days=30)

    # 2) ջնջել այսօր գրանցված event-ները, որ սեղմ refresh լինի
    today = date.today().isoformat()
    _delete_today_events(today)

    # 3) Լցնել այսօրվա data-ն ըստ ուղղությունների

    # 3.1 Կինո (real data Tomsarkgh-ից)
    for ev in fetch_cinema_from_tomsarkgh(limit=15):
        save_event(ev)

    # Եթե ուզում ես ժամանակավորապես նաև dummy թողնել՝ comment չանես.
    # for ev in get_dummy_film_events():
    #     save_event(ev)

    # 3.2 Թատրոն / օպերա / փաբ / event-ներ
    # Հիմա դեռ ոչինչ չենք լցնում, հետո այստեղ կկանչենք իրական source fetch-եր
    # օրինակ.
    # for ev in await fetch_theatre_from_tomsarkgh():
    #     save_event(ev)
    # ....


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
