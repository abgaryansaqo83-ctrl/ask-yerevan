from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
from backend.admin_routes import router as admin_router
from backend.churches_data import CHURCHES
from backend.sights_data import SIGHTS
from backend.places_data import PLACES
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date
from pathlib import Path
import uuid

from backend.database import (
    init_db,
    get_all_news,
    get_news_by_id,
    get_random_news_with_image,
    toggle_place_like,
    get_place_likes,
    set_place_rating,
    get_place_rating,
    add_place_comment,
    get_place_comments,
    get_place_comment_count,
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
        "sights_list_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "sights": SIGHTS,
        },
    )

@app.get("/hy/sights/{sight_id}", response_class=HTMLResponse)
async def sight_detail_hy(request: Request, sight_id: str):
    sight = next((s for s in SIGHTS if s["id"] == sight_id), None)
    if not sight:
        return RedirectResponse(url="/hy/sights")
    return templates.TemplateResponse(
        "sights_detail_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "sight": sight,
            "back_url": "/hy/sights",
        },
    )

@app.get("/en/sights", response_class=HTMLResponse)
async def sights_en(request: Request):
    return templates.TemplateResponse(
        "sights_list_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "sights": SIGHTS,
        },
    )

@app.get("/en/sights/{sight_id}", response_class=HTMLResponse)
async def sight_detail_en(request: Request, sight_id: str):
    sight = next((s for s in SIGHTS if s["id"] == sight_id), None)
    if not sight:
        return RedirectResponse(url="/en/sights")
    return templates.TemplateResponse(
        "sights_detail_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "sight": sight,
            "back_url": "/en/sights",
        },
    )

# ════════════════════════════════
# Places
# ════════════════════════════════

def get_place_by_id(place_id: str):          # 1. helper
    return next((p for p in PLACES if p["id"] == place_id), None)

@app.get("/hy/places", response_class=HTMLResponse)
async def places_list_hy(request: Request):
    return templates.TemplateResponse(
        "places_list_hy.html",
        {
            "request":         request,
            "lang":            "hy",
            "places":          PLACES,
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )


@app.get("/en/places", response_class=HTMLResponse)
async def places_list_en(request: Request):
    return templates.TemplateResponse(
        "places_list_en.html",
        {
            "request":         request,
            "lang":            "en",
            "places":          PLACES,
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )
    
@app.get("/hy/places/{place_id}", response_class=HTMLResponse)
async def place_detail_hy(request: Request, place_id: str):
    place = get_place_by_id(place_id)
    if not place:
        return RedirectResponse(url="/hy/places")
    return templates.TemplateResponse(
        "places_detail_hy.html",
        {
            "request":         request,
            "lang":            "hy",
            "place":           place,
            "backurl":         "/hy/places",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

@app.get("/en/places/{place_id}", response_class=HTMLResponse)
async def place_detail_en(request: Request, place_id: str):
    place = get_place_by_id(place_id)
    if not place:
        return RedirectResponse(url="/en/places")
    return templates.TemplateResponse(
        "places_detail_en.html",
        {
            "request":         request,
            "lang":            "en",
            "place":           place,
            "backurl":         "/en/places",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# ════════════════════════════════
# Places API (likes / ratings / comments)
# ════════════════════════════════

def get_or_create_session(request: Request, response: JSONResponse) -> str:
    session_id = request.cookies.get("place_session")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="place_session",
            value=session_id,
            max_age=60 * 60 * 24 * 365,  # 1 տարի
            httponly=True,
            samesite="lax",
        )
    return session_id


@app.post("/api/places/{place_id}/like")
async def api_place_like(place_id: str, request: Request):
    response = JSONResponse(content={})
    session_id = request.cookies.get("place_session") or str(uuid.uuid4())
    result = toggle_place_like(place_id, session_id)
    resp = JSONResponse(content=result)
    resp.set_cookie(
        key="place_session",
        value=session_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
    )
    return resp


@app.get("/api/places/{place_id}/likes")
async def api_place_likes(place_id: str, request: Request):
    session_id = request.cookies.get("place_session") or ""
    result = get_place_likes(place_id, session_id)
    return JSONResponse(content=result)


@app.post("/api/places/{place_id}/rating")
async def api_place_rating_set(place_id: str, request: Request):
    body = await request.json()
    rating = int(body.get("rating", 0))
    if not 1 <= rating <= 5:
        return JSONResponse(content={"error": "Invalid rating"}, status_code=400)
    session_id = request.cookies.get("place_session") or str(uuid.uuid4())
    result = set_place_rating(place_id, session_id, rating)
    resp = JSONResponse(content=result)
    resp.set_cookie(
        key="place_session",
        value=session_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
    )
    return resp


@app.get("/api/places/{place_id}/rating")
async def api_place_rating_get(place_id: str, request: Request):
    session_id = request.cookies.get("place_session") or ""
    result = get_place_rating(place_id, session_id)
    return JSONResponse(content=result)


@app.post("/api/places/{place_id}/comments")
async def api_place_comment_add(place_id: str, request: Request):
    body = await request.json()
    text = str(body.get("text", "")).strip()
    rating = int(body.get("rating", 0))
    if not text:
        return JSONResponse(content={"error": "Empty comment"}, status_code=400)
    session_id = request.cookies.get("place_session") or str(uuid.uuid4())
    result = add_place_comment(place_id, session_id, text, rating)
    resp = JSONResponse(content=result)
    resp.set_cookie(
        key="place_session",
        value=session_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
    )
    return resp


@app.get("/api/places/{place_id}/comments")
async def api_place_comments_get(place_id: str):
    comments = get_place_comments(place_id)
    for c in comments:
        if hasattr(c.get("created_at"), "isoformat"):
            c["created_at"] = c["created_at"].isoformat()
    return JSONResponse(content=comments)
    
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
