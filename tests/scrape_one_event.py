import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


EVENT_URL = "https://www.tomsarkgh.am/hy/event/49688/%D4%B3%D5%B8%D5%B2%D5%B8%D6%82%D5%A9%D5%B5%D5%B8%D6%82%D5%B6-%D5%B0%D5%A1%D5%B5%D5%AF%D5%A1%D5%AF%D5%A1%D5%B6-%D5%B1%D6%87%D5%B8%D5%BE.html"


def scrape_one_event(url: str) -> dict:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Վերնագիր
    title_tag = soup.select_one("h1.event-name")
    title = title_tag.get_text(strip=True) if title_tag else "Без названия"

    # Առաջին սեսիայի օրն ու ժամը
    start_meta = soup.select_one("meta[itemprop=startDate]")
    raw_dt = start_meta["content"].strip() if start_meta and start_meta.has_attr("content") else ""
    # content ձևաչափը մոտավորապես "2025-12-03 22:00"
    date_part, time_part = None, None
    if " " in raw_dt:
        date_part, time_part = raw_dt.split(" ", 1)
    else:
        date_part = raw_dt

    # Վայրը (կինոթատրոնի անունը)
    venue_span = soup.select_one("div.occurrence_venue span[itemprop=name]")
    place = venue_span.get_text(strip=True) if venue_span else "Unknown venue"

    event = {
        "title": title,
        "date": date_part,
        "time": time_part,
        "place": place,
        "city": "Yerevan",
        "category": "cinema",
        "url": url,
        "source": "tomsarkgh",
    }
    return event


if __name__ == "__main__":
    data = scrape_one_event(EVENT_URL)
    print(data)
