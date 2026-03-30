import os
import shutil
import unicodedata
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import save_news, get_news_by_id, update_news

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "askyerevan2026")
UPLOAD_DIR = "static/img/important"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def make_safe_filename(title: str, ext: str) -> str:
    title = unicodedata.normalize('NFKD', title)
    title = title.encode('ascii', 'ignore').decode('ascii')
    safe = ''.join(c if c.isalnum() else '-' for c in title[:30].strip().lower())
    return f"{safe}.{ext}"

def is_logged_in(request: Request) -> bool:
    return request.cookies.get("admin_auth") == ADMIN_PASSWORD

@router.get("/admin", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    if is_logged_in(request):
        return RedirectResponse("/admin/panel")
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "page": "login",
        "error": None
    })

@router.post("/admin/login")
async def admin_login(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse("/admin/panel", status_code=302)
        response.set_cookie("admin_auth", ADMIN_PASSWORD, httponly=True)
        return response
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "page": "login",
        "error": "Սխալ գաղտնաբառ"
    })

@router.get("/admin/panel", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not is_logged_in(request):
        return RedirectResponse("/admin")
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "page": "panel",
        "success": None,
        "error": None
    })

@router.post("/admin/publish", response_class=HTMLResponse)
async def admin_publish(
    request: Request,
    title_hy: str = Form(...),
    title_en: str = Form(...),
    content_hy: str = Form(...),
    content_en: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None),
    image_url_manual: str = Form(""),
    image_2: str = Form(""),
    image_3: str = Form(""),
    video_url: str = Form(""),
):
    if not is_logged_in(request):
        return RedirectResponse("/admin")

    image_url = None

    if image and image.filename:
        ext = image.filename.rsplit(".", 1)[-1].lower()
        filename = make_safe_filename(title_en, ext)
        filepath = f"{UPLOAD_DIR}/{filename}"
        with open(filepath, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_url = f"/static/img/important/{filename}"
    elif image_url_manual.strip():
        image_url = image_url_manual.strip()

    try:
        news_id = save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=category,
            image_2=image_2.strip() or None,
            image_3=image_3.strip() or None,
            video_url=video_url.strip() or None,
        )
        return templates.TemplateResponse("admin_panel.html", {
            "request": request,
            "page": "panel",
            "success": f"Հրապարակվեց։ ID {news_id} — /hy/news/{news_id}",
            "error": None
        })
    except Exception as e:
        return templates.TemplateResponse("admin_panel.html", {
            "request": request,
            "page": "panel",
            "success": None,
            "error": str(e)
        })

@router.get("/admin/edit/{news_id}", response_class=HTMLResponse)
async def admin_edit_page(request: Request, news_id: int):
    if not is_logged_in(request):
        return RedirectResponse("/admin")
    news = get_news_by_id(news_id)
    if not news:
        return HTMLResponse("Նորությունը չի գտնվել", status_code=404)
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "page": "edit",
        "news": dict(news),
        "success": None,
        "error": None
    })

@router.post("/admin/edit/{news_id}", response_class=HTMLResponse)
async def admin_edit_submit(
    request: Request,
    news_id: int,
    title_hy: str = Form(...),
    title_en: str = Form(...),
    content_hy: str = Form(...),
    content_en: str = Form(...),
    category: str = Form(...),
    image_url_manual: str = Form(""),
    eventdate: str = Form(""),
    eventtime: str = Form(""),
    venue_hy: str = Form(""),
    price_hy: str = Form(""),
    image_2: str = Form(""),
    image_3: str = Form(""),
    video_url: str = Form(""),
    image: UploadFile = File(None),
):
    if not is_logged_in(request):
        return RedirectResponse("/admin")

    existing = get_news_by_id(news_id)
    image_url = existing["image_url"] if existing else None

    if image and image.filename:
        ext = image.filename.rsplit(".", 1)[-1].lower()
        filename = make_safe_filename(title_en, ext)
        filepath = f"{UPLOAD_DIR}/{filename}"
        with open(filepath, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_url = f"/static/img/important/{filename}"
    elif image_url_manual.strip():
        image_url = image_url_manual.strip()

    updated = update_news(
        news_id=news_id,
        title_hy=title_hy,
        title_en=title_en,
        content_hy=content_hy,
        content_en=content_en,
        image_url=image_url,
        category=category,
        eventdate=eventdate or None,
        eventtime=eventtime or None,
        venue_hy=venue_hy or None,
        price_hy=price_hy or None,
        image_2=image_2.strip() or None,
        image_3=image_3.strip() or None,
        video_url=video_url.strip() or None,
    )

    news = get_news_by_id(news_id)
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "page": "edit",
        "news": dict(news),
        "success": f"Թարմացվեց։ ID {news_id}" if updated else None,
        "error": None if updated else "Թարմացումը չհաջողվեց"
    })
    
@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse("/admin")
    response.delete_cookie("admin_auth")
    return response
