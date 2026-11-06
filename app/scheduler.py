# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/scheduler.py
# FUNGSI  : Menjalankan posting terjadwal
# ============================================

import asyncio
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models import Draft
from app.services.publisher import publish_draft

async def scheduler_loop():
    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)
            due = db.query(Draft).filter(Draft.status == "scheduled", Draft.scheduled_at <= now).limit(10).all()
            ids = [d.id for d in due]
            for draft_id in ids:
                try: await publish_draft(draft_id)
                except Exception: pass
        finally:
            db.close()
        await asyncio.sleep(20)
