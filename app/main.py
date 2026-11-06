# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/main.py
# FUNGSI  : Entry point FastAPI dan Mini App
# ============================================

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import init_db, SessionLocal
from app.config import settings
from app.models import Admin
from app.scheduler import scheduler_loop
from app.api import history, drafts, destinations, admins

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        primary = db.get(Admin, settings.primary_admin_id)
        if not primary:
            db.add(Admin(id=settings.primary_admin_id, is_primary=True))
            db.commit()
    finally: db.close()
    task = asyncio.create_task(scheduler_loop())
    yield
    task.cancel()

app = FastAPI(title="NEXORA RICH MESSAGE BOT", version="1.0.0", lifespan=lifespan)
app.include_router(history.router)
app.include_router(drafts.router)
app.include_router(destinations.router)
app.include_router(admins.router)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    return (static_dir / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health(): return {"ok": True, "service": "nexora-api"}
