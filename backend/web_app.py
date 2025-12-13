from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AskYerevan Web")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root՝ always դեպի հայերեն
@app.get("/", response_class=HTMLResponse)
async def root_redirect(request: Request):
  return RedirectResponse(url="/hy")

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

@app.get("/hy/events", response_class=HTMLResponse)
async def events_hy(request: Request):
  return templates.TemplateResponse(
      "events_hy.html",
      {"request": request, "lang": "hy"}
  )

@app.get("/en/events", response_class=HTMLResponse)
async def events_en(request: Request):
  return templates.TemplateResponse(
      "events_en.html",
      {"request": request, "lang": "en"}
  )

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

@app.get("/health")
async def health():
  return {"status": "ok"}
