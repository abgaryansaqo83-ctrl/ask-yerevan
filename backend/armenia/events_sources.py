# backend/armenia/events_sources.py

from datetime import datetime
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup


# ---------- Real fetchers from Tomsarkgh (LIVE) ----------

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

    # Սկզբի ամսաթիվ/ժամ (ISO datetime կամ date)
    start_meta = soup.select_one("meta[itemprop=startDate]")
    raw_dt = start_meta["content"].strip() if start_meta and start_meta.has_attr("content") else ""
    date_part, time_part = None, None
    if " " in raw_dt:
        date_part, time_part = raw_dt.split(" ", 1)
    else:
        date_part = raw_dt or None

    if not date_part:
        return None

    # Վայրը
    venue_span = soup.select_one("div.occurrence_venue span[itemprop=name]")
    place = venue_span.get_text(strip=True) if venue_span else "Unknown venue"

    # Գին (փորձում ենք գտնել price block-ը, եթե չկա՝ թողնում ենք placeholder)
    price_block = soup.select_one(".event-price, .event_prices, .prices, .event-price-block")
    if price_block:
        price_text = price_block.get_text(strip=True)
    else:
        price_text = "գինը նշված չէ"

    return {
        "title": title,
        "date": date_part,
        "time": time_part,
        "place": place,
        "city": "Yerevan",
        "price": price_text,
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
    """Կինոների category էջից քաշում է մինչև `limit` ֆիլմերի event-ներ (LIVE)."""
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(CINEMA_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "cinema"
            events.append(ev)

    return events


def fetch_theatre_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """Թատրոնի բաժնի event-ներ (LIVE)."""
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(THEATRE_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "theatre"
            events.append(ev)
    return events


def fetch_opera_from_tomsarkgh(limit: int = 10) -> List[Dict[str, Any]]:
    """Օպերա / բալետ բաժնի event-ներ (LIVE)."""
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(OPERA_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "opera"
            events.append(ev)
    return events


def fetch_party_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """Ակումբ / փաբ / party բաժնի nightlife event-ներ (LIVE)."""
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(PARTY_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "party"
            events.append(ev)
    return events


def fetch_misc_events_from_tomsarkgh(limit: int = 20) -> List[Dict[str, Any]]:
    """«Այլ» բաժնի stand‑up, ցուցահանդես և նման event-ներ (LIVE)."""
    events: List[Dict[str, Any]] = []
    links = _collect_event_links(EVENTS_CATEGORY_URL, limit=limit)

    for url in links:
        ev = _scrape_one_tomsarkgh_event(url)
        if ev is not None:
            ev["category"] = "festival"  # generic cultural events
            events.append(ev)
    return events


# ---------- Aggregated LIVE fetcher for /news ----------

def fetch_live_events_for_category(kind: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Վերադարձնում է LIVE event-ների list տվյալ kind-ի համար՝
    անմիջապես Tomsarkgh-ից, առանց DB-ի:
      kind: cinema / theatre / opera / party / festival
    """
    if kind == "cinema":
        events = fetch_cinema_from_tomsarkgh(limit=limit)
    elif kind == "theatre":
        events = fetch_theatre_from_tomsarkgh(limit=limit)
    elif kind == "opera":
        events = fetch_opera_from_tomsarkgh(limit=limit)
    elif kind == "party":
        events = fetch_party_from_tomsarkgh(limit=limit)
    elif kind == "festival":
        events = fetch_misc_events_from_tomsarkgh(limit=limit)
    else:
        events = []

    # sort by date/time asc, որ մոտակա օրերն առաջնահերթ գան
    def _dt_key(ev: Dict[str, Any]):
        d = ev.get("date") or ""
        t = ev.get("time") or ""
        try:
            if t:
                return datetime.fromisoformat(f"{d} {t}")
            return datetime.fromisoformat(d)
        except Exception:
            return datetime.max

    events.sort(key=_dt_key)
    return events
