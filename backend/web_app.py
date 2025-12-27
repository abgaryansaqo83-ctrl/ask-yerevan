from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Query
from datetime import date
from backend.database import get_all_news, init_db
from backend.database import get_all_news, get_news_by_id

# ✅ Add logger
import logging
logger = logging.getLogger(__name__)

# ✅ Initialize database
try:
    init_db()
    logger.info("✅ Database initialized successfully")
    print("✅ Database initialized successfully")  # Console output
except Exception as e:
    logger.error(f"❌ Database initialization failed: {e}")
    print(f"❌ Database initialization failed: {e}")

app = FastAPI(title="AskYerevan Web")

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

# Root — միշտ ռիդիրեքթ հայերեն գլխավոր
@app.get("/", response_class=HTMLResponse)
async def root_redirect(request: Request):
    return RedirectResponse(url="/hy")

# Գլխավոր էջ
@app.get("/hy", response_class=HTMLResponse)
async def index_hy(request: Request):
    return templates.TemplateResponse(
        "index_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

@app.get("/en", response_class=HTMLResponse)
async def index_en(request: Request):
    return templates.TemplateResponse(
        "index_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# Եկեղեցիներ
@app.get("/hy/churches", response_class=HTMLResponse)
async def churches_hy(request: Request):
    return templates.TemplateResponse(
        "churches_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

@app.get("/en/churches", response_class=HTMLResponse)
async def churches_en(request: Request):
    return templates.TemplateResponse(
        "churches_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
        },
    )

# Նորություններ
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
            "category": category  # ← Pass to template for active state
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
            "category": category
        },
    )

# Single news page — HY
@app.get("/hy/news/{news_id}", response_class=HTMLResponse)
async def news_detail_hy(request: Request, news_id: int):
    news_item = get_news_by_id(news_id)
    
    if not news_item:
        return RedirectResponse(url="/hy/news")
    
    return templates.TemplateResponse(
        "news_detail_hy.html",
        {
            "request": request,
            "lang": "hy",
            "is_winter_theme": is_winter_theme_enabled(),
            "news": news_item
        },
    )

# Single news page — EN
@app.get("/en/news/{news_id}", response_class=HTMLResponse)
async def news_detail_en(request: Request, news_id: int):
    news_item = get_news_by_id(news_id)
    
    if not news_item:
        return RedirectResponse(url="/en/news")
    
    return templates.TemplateResponse(
        "news_detail_en.html",
        {
            "request": request,
            "lang": "en",
            "is_winter_theme": is_winter_theme_enabled(),
            "news": news_item
        },
    )
    
# Տեսարժան վայրեր
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

# Ժամանցի վայրեր
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

# Խմբի մասին
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
