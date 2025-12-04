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


# ---------- Real fetchers from Tomsarkgh ----------

CINEMA_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D4%BF%D5%AB%D5%B6%D5%B8"
THEATRE_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D4%B9%D5%A1%D5%BF%D6%80%D5%B8%D5%B6"
OPERA_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D5%95%D5%BA%D5%A5%D6%80%D5%A1-%D6%87-%D5%A2%D5%A1%D5%AC%D5%A5%D5%BF"
PARTY_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D4%B1%D5%AF%D5%B8%D6%82%D5%B4%D5%A2-%D6%87-%D6%83%D5%A1%D5%A2"
EVENTS_CATEGORY_URL = "https://www.tomsarkgh.am/hy/category/%D4%B1%D5%B5%D5%AC"


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
        "category": "cinema",  # default, հետո fetch_*-երը կփոխեն
        "url": url,
        "source": "tomsarkgh",
    }


def _collect_event_links(category_url: str, limit: int) -> list[str]:
    """
    Բացում է տրված category_url-ը և վերադարձնում մինչև limit event URL-ների list։
    Օգտագործվում է կինո/թատրոն/օպերա/փաբ և այլն fetch-երում։
    """
    links: list[str] = []

    try:
        resp = requests.get(category_url, timeout=15)
    except Exception:
        return links

    if resp.status_code != 200:
        return links

    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.select('a[href^="/hy/event/"]'):
        href = a.get("href")
        if not href:
            continue
        full_url = "https://www.tomsarkgh.am" + href
        if full_url not in links:
            links.append(full_url)
        if len(links) >= limit:
            break

    return links


def fetch_cinema_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Կինոների category էջից քաշում է մինչև `limit` ֆիլմերի event-ներ։
    """
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(CINEMA_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "cinema"
            events.append(ev)

    return events


def fetch_theatre_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(THEATRE_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "theatre"
            events.append(ev)
    return events


def fetch_opera_from_tomsarkgh(limit: int = 10) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(OPERA_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "opera"
            events.append(ev)
    return events


def fetch_party_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Ակումբ/փաբ/party բաժինից ընդհանուր nightlife event-ներ։
    """
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(PARTY_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "party"
            events.append(ev)
    return events


def fetch_misc_events_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """
    «Այլ» բաժնի stand-up, ցուցահանդես և նման event-ներ։
    """
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(EVENTS_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "festival"  # կամ "other"՝ ինչպես կուզես DB-ում պահել
            events.append(ev)
    return events


# ---------- ՇԱԲԱԹԱԿԱՆ REFRESH (երկուշաբթի 03:00) ----------

async def refresh_week_events():
    """
    Ամեն երկուշաբթի 03:00.
    - Մաքրում է 14 օրից հին event-ները;
    - Քաշում է Tomsarkgh-ից առաջիկա օրերի event-ները
      բոլոր հիմնական կատեգորիաների համար (մինչև 20 event մեկ կատեգորիայում) և
      պահում է DB-ում:
    """

    # 1) ջնջել 14 օրից հին event-ները
    cleanup_old_events(days=14)

    # Եթե ուզում ես լիովին նստարք անել ու ամեն շաբաթ զրոյից լցնել՝
    # _delete_all_events()

    # 2) Քաշել նոր շաբաթվա event-ները ըստ ուղղությունների

    # Կինո
    for ev in fetch_cinema_from_tomsarkgh(limit=20):
        save_event(ev)

    # Թատրոն
    for ev in fetch_theatre_from_tomsarkgh(limit=20):
        save_event(ev)

    # Օպերա / բալետ
    for ev in fetch_opera_from_tomsarkgh(limit=10):
        save_event(ev)

    # Ակումբ / փաբ / party
    for ev in fetch_party_from_tomsarkgh(limit=20):
        save_event(ev)

    # Այլ event-ներ (stand-up, ցուցահանդես և այլն)
    for ev in fetch_misc_events_from_tomsarkgh(limit=20):
        save_event(ev)


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
