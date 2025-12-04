import requests
from bs4 import BeautifulSoup

EVENT_URL = "https://www.tomsarkgh.am/hy/event/49890/Մոլորվածը.html"

def scrape_one_event(url: str) -> dict:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one("h1.event-name")
    title = title_tag.get_text(strip=True) if title_tag else "Без названия"

    start_meta = soup.select_one("meta[itemprop=startDate]")
    raw_dt = start_meta["content"].strip() if start_meta and start_meta.has_attr("content") else ""
    date_part, time_part = None, None
    if " " in raw_dt:
        date_part, time_part = raw_dt.split(" ", 1)
    else:
        date_part = raw_dt

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


if __name__ == "__main__":
    print(scrape_one_event(EVENT_URL))
