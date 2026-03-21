from fastapi import FastAPI, Request, Query
from backend.admin_routes import router as admin_router
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date
from pathlib import Path  # <-- ԱՎԵԼԱՑՎԱԾ

from backend.database import (
    init_db,
    get_all_news,
    get_news_by_id,
    get_random_news_with_image,
)

import logging

logger = logging.getLogger(__name__)

# Init DB once on startup
try:
    init_db()
    logger.info("✅ Database initialized successfully")
    print("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {e}")
    print(f"❌ Database initialization failed: {e}")

# ============================================================
# CHURCHES DATA
# ============================================================
CHURCHES = [
    {
        "id": "echmiadzin_cathedral",
        "name_hy": "Էջմիածնի մայր տաճար",
        "name_en": "Etchmiadzin Cathedral",
        "century": "4-րդ դար",
        "year": 301,
        "location_hy": "Վաղարշապատ (Էջմիածին), Արմավիրի մարզ",
        "location_en": "Vagharshapat (Etchmiadzin), Armavir region",
        "address_hy": "Վաղարշապատ, Էջմիածնի մայր տաճար",
        "address_en": "Vagharshapat, Mother Cathedral of Etchmiadzin",
        "unesco": True,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=40.1596,44.2919",
        "image_main": "/static/img/churches/etchmiadzin-old-1.jpg",
        "image_old": "/static/img/churches/etchmiadzin-old-1.jpg",
        "image_new": "/static/img/churches/etchmiadzin-old-2.jpg",
    },
    {
        "id": "zvartnots",
        "name_hy": "Զվարթնոց տաճար",
        "name_en": "Zvartnots Cathedral",
        "century": "7-րդ դար",
        "year": 643,
        "location_hy": "Զվարթնոց, Արմավիրի մարզ",
        "location_en": "Zvartnots, Armavir region",
        "address_hy": "Զվարթնոց հնագիտական համալիր",
        "address_en": "Zvartnots Archaeological Site",
        "unesco": True,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=40.1540,44.2354",
        "image_main": "/static/img/churches/artashat-octagon-1.jpg",
        "image_old": "/static/img/churches/artashat-octagon-1.jpg",
        "image_new": "/static/img/churches/artashat-octagon-2.jpg",
    },
    {
        "id": "khor_virap",
        "name_hy": "Խոր Վիրապ վանք",
        "name_en": "Khor Virap Monastery",
        "century": "17-րդ դար (ներկայիս complex)",
        "year": 1662,
        "location_hy": "Արարատի մարզ, Արտաշատին մոտ",
        "location_en": "Ararat region, near Artashat",
        "address_hy": "Արարատի մարզ, Խոր Վիրապ",
        "address_en": "Khor Virap, Ararat region",
        "unesco": False,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=39.8284,44.5619",
        "image_main": "/static/img/churches/khor-virap-new.jpg",
        "image_old": "/static/img/churches/khor-virap-old.jpg",
        "image_new": "/static/img/churches/khor-virap-new.jpg",
    },
    {
        "id": "geghard",
        "name_hy": "Գեղարդի վանք",
        "name_en": "Geghard Monastery",
        "century": "13-րդ դար",
        "year": 1215,
        "location_hy": "Կոտայքի մարզ, Ազատ գետի կիրճ",
        "location_en": "Kotayk region, Azat River gorge",
        "address_hy": "Կոտայքի մարզ, Գեղարդավանք",
        "address_en": "Geghard Monastery, Kotayk region",
        "unesco": True,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=40.1415,44.8143",
        "image_main": "/static/img/churches/geghard-outside-main.jpg",
        "image_old": "/static/img/churches/Geghard-qarer.jpg",
        "image_new": "/static/img/churches/geghard-outside-main.jpg",
    },
    {
        "id": "noravank",
        "name_hy": "Նորավանք վանք",
        "name_en": "Noravank Monastery",
        "century": "13-րդ դար",
        "year": 1205,
        "location_hy": "Վայոց ձոր, Ամաղու գյուղի մոտ",
        "location_en": "Vayots Dzor, near Amaghu village",
        "address_hy": "Վայոց ձոր, Նորավանք",
        "address_en": "Noravank, Vayots Dzor",
        "unesco": False,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=39.6836,45.2311",
        "image_main": "/static/img/churches/noravank-new.jpg",
        "image_old": "/static/img/churches/noravank-old.jpg",
        "image_new": "/static/img/churches/noravank-new.jpg",
    },
]

app = FastAPI(title="AskYerevan Web")
app.include_router(admin_router)


def is_winter_theme_enabled() -> bool:
    today = date.today()
    year = today.year

    start = date(year, 12, 20)
    end = date(year + 1, 1, 15)

    if today >= start:
        return today <= end
    else:
        prev_start = date(year - 1, 12, 20)
        prev_end = date(year, 1, 15)
        return prev_start <= today <= prev_end


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- SITEMAP CONFIG -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SITEMAP_PATH = BASE_DIR / "sitemap.xml"


@app.get("/sitemap.xml", response_class=Response)
def sitemap():
    """
    Return static sitemap.xml from project root.
    """
    xml_content = SITEMAP_PATH.read_text(encoding="utf-8")
    return Response(content=xml_content, media_type="application/xml")

# --------------------------------------------------------------------

# Root → redirect HY
@app.get("/", response_class=HTMLResponse)
async def root_redirect(request: Request):
    return RedirectResponse(url="/hy")

# Index
@app.get("/hy", response_class=HTMLResponse)
async def indexhy(request: Request):
    hero_events = get_random_news_with_image("events")
    hero_city = get_random_news_with_image("city")
    hero_culture = get_random_news_with_image("culture")

    return templates.TemplateResponse(
        "index_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "hero_events": hero_events,
            "hero_city": hero_city,
            "hero_culture": hero_culture,
        },
    )


@app.get("/en", response_class=HTMLResponse)
async def indexen(request: Request):
    hero_events = get_random_news_with_image("events")
    hero_city = get_random_news_with_image("city")
    hero_culture = get_random_news_with_image("culture")

    return templates.TemplateResponse(
        "index_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "hero_events": hero_events,
            "hero_city": hero_city,
            "hero_culture": hero_culture,
        },
    )

# Churches
@app.get("/hy/churches", response_class=HTMLResponse)
async def churches_hy(request: Request):
    return templates.TemplateResponse(
        "churches_list_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "churches": CHURCHES,
        },
    )


@app.get("/hy/churches/{church_id}", response_class=HTMLResponse)
async def church_detail_hy(request: Request, church_id: str):
    church = next((c for c in CHURCHES if c["id"] == church_id), None)
    if not church:
        return RedirectResponse(url="/hy/churches")
    return templates.TemplateResponse(
        "church_detail_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "church": church,
            "back_url": "/hy/churches",
        },
    )


@app.get("/en/churches", response_class=HTMLResponse)
async def churches_en(request: Request):
    return templates.TemplateResponse(
        "churches_list_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "churches": CHURCHES,
        },
    )


@app.get("/en/churches/{church_id}", response_class=HTMLResponse)
async def church_detail_en(request: Request, church_id: str):
    church = next((c for c in CHURCHES if c["id"] == church_id), None)
    if not church:
        return RedirectResponse(url="/en/churches")
    return templates.TemplateResponse(
        "church_detail_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "church": church,
            "back_url": "/en/churches",
        },
    )


# News list
@app.get("/hy/news", response_class=HTMLResponse)
async def news_hy(request: Request, category: str = Query(None)):
    news_list = get_all_news(limit=50, category=category)
    return templates.TemplateResponse(
        "news_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "news_list": news_list,
            "category": category,
        },
    )


@app.get("/en/news", response_class=HTMLResponse)
async def news_en(request: Request, category: str = Query(None)):
    news_list = get_all_news(limit=50, category=category)
    return templates.TemplateResponse(
        "news_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "news_list": news_list,
            "category": category,
        },
    )

# Single news HY
@app.get("/hy/news/{news_id}", response_class=HTMLResponse)
async def news_detail_hy(request: Request, news_id: int):
    news_item = get_news_by_id(news_id)
    if not news_item:
        return RedirectResponse(url="/hy/news")

    category = (
        news_item.get("category")
        if isinstance(news_item, dict)
        else getattr(news_item, "category", None)
    )
    back_url = "/hy/news"
    if category:
        back_url = f"/hy/news?category={category}"

    return templates.TemplateResponse(
        "news_detail_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "news": news_item,
            "back_url": back_url,
        },
    )

# Single news EN
@app.get("/en/news/{news_id}", response_class=HTMLResponse)
async def news_detail_en(request: Request, news_id: int):
    news_item = get_news_by_id(news_id)
    if not news_item:
        return RedirectResponse(url="/en/news")

    category = (
        news_item.get("category")
        if isinstance(news_item, dict)
        else getattr(news_item, "category", None)
    )
    back_url = "/en/news"
    if category:
        back_url = f"/en/news?category={category}"

    return templates.TemplateResponse(
        "news_detail_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "news": news_item,
            "back_url": back_url,
        },
    )

# Sights
@app.get("/hy/sights", response_class=HTMLResponse)
async def sights_hy(request: Request):
    return templates.TemplateResponse(
        "sights_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )


@app.get("/en/sights", response_class=HTMLResponse)
async def sights_en(request: Request):
    return templates.TemplateResponse(
        "sights_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# Places
@app.get("/hy/places", response_class=HTMLResponse)
async def places_hy(request: Request):
    return templates.TemplateResponse(
        "places_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )


@app.get("/en/places", response_class=HTMLResponse)
async def places_en(request: Request):
    return templates.TemplateResponse(
        "places_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# About
@app.get("/hy/about", response_class=HTMLResponse)
async def about_hy(request: Request):
    return templates.TemplateResponse(
        "about_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )


@app.get("/en/about", response_class=HTMLResponse)
async def about_en(request: Request):
    return templates.TemplateResponse(
        "about_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# Healthcheck
@app.get("/health")
async def health():
    return {"status": "ok"}
