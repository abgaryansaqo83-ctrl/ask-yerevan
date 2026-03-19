import os
import shutil
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import save_news

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "askyerevan2026")
UPLOAD_DIR = "static/img/important"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
    image_url_manual: str = Form("")
):
    if not is_logged_in(request):
        return RedirectResponse("/admin")

    image_url = None

    # եթե ֆայլ upload արվել է
    if image and image.filename:
        ext = image.filename.rsplit(".", 1)[-1].lower()
        safe_title = title_en[:30].strip().lower()
        safe_title = "".join(c if c.isalnum() else "-" for c in safe_title)
        filename = f"{safe_title}.{ext}"
        filepath = f"{UPLOAD_DIR}/{filename}"
        with open(filepath, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_url = f"/static/img/important/{filename}"

    # եթե manual URL է տրված
    elif image_url_manual.strip():
        image_url = image_url_manual.strip()

    try:
        news_id = save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=category
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


@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse("/admin")
    response.delete_cookie("admin_auth")
    return response
