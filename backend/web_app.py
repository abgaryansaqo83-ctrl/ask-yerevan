from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AskYerevan Web")
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
        {"request": request, "lang": "hy"}
    )

@app.get("/en", response_class=HTMLResponse)
async def index_en(request: Request):
    return templates.TemplateResponse(
        "index_en.html",
        {"request": request, "lang": "en"}
    )

# Եկեղեցիներ
@app.get("/hy/churches", response_class=HTMLResponse)
async def churches_hy(request: Request):
    return templates.TemplateResponse(
        "churches_hy.html",
        {"request": request, "lang": "hy"}
    )

@app.get("/en/churches", response_class=HTMLResponse)
async def churches_en(request: Request):
    return templates.TemplateResponse(
        "churches_en.html",
        {"request": request, "lang": "en"}
    )

# Նորություններ
@app.get("/hy/news", response_class=HTMLResponse)
async def news_hy(request: Request):
    return templates.TemplateResponse(
        "events_hy.html",          # ֆայլը՝ նորությունների template
        {"request": request, "lang": "hy"}
    )

@app.get("/en/news", response_class=HTMLResponse)
async def news_en(request: Request):
    return templates.TemplateResponse(
        "events_en.html",
        {"request": request, "lang": "en"}
    )

# Տեսարժան վայրեր
@app.get("/hy/sights", response_class=HTMLResponse)
async def sights_hy(request: Request):
    return templates.TemplateResponse(
        "sights_hy.html",
        {"request": request, "lang": "hy"}
    )

@app.get("/en/sights", response_class=HTMLResponse)
async def sights_en(request: Request):
    return templates.TemplateResponse(
        "sights_en.html",
        {"request": request, "lang": "en"}
    )

# Ժամանցի վայրեր
@app.get("/hy/places", response_class=HTMLResponse)
async def places_hy(request: Request):
    return templates.TemplateResponse(
        "places_hy.html",
        {"request": request, "lang": "hy"}
    )

@app.get("/en/places", response_class=HTMLResponse)
async def places_en(request: Request):
    return templates.TemplateResponse(
        "places_en.html",
        {"request": request, "lang": "en"}
    )

# Խմբի մասին
@app.get("/hy/about", response_class=HTMLResponse)
async def about_hy(request: Request):
    return templates.TemplateResponse(
        "about_hy.html",
        {"request": request, "lang": "hy"}
    )

@app.get("/en/about", response_class=HTMLResponse)
async def about_en(request: Request):
    return templates.TemplateResponse(
        "about_en.html",
        {"request": request, "lang": "en"}
    )

# Healthcheck
@app.get("/health")
async def health():
    return {"status": "ok"}
