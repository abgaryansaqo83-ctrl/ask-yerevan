# backend/web_app.py

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from backend.utils.logger import logger

app = FastAPI(title="AskYerevan Web")

@app.on_event("startup")
async def on_startup():
    logger.info("🌐 AskYerevan Web Service started")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
      <head><title>AskYerevan</title></head>
      <body>
        <h1>AskYerevan Web Service</h1>
        <p>Bot & background jobs are running.</p>
      </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok"}
