# backend/web_app.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AskYerevan Web")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/events", response_class=HTMLResponse)
async def events_page(request: Request):
    # ուզում ես՝ այստեղ կարող ես կպցնել get_events_by_category(...),
    # չի ուզում՝ թող մաքուր ձեռքով գրված content լինի template-ում
    return templates.TemplateResponse("events.html", {"request": request})

@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok"}
