# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/api/history.py
# FUNGSI  : Posting History API
# ============================================

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PostingHistory
from app.api.deps import get_user

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("")
def list_history(limit: int = 50, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    rows = db.query(PostingHistory).filter(PostingHistory.admin_id == int(user["id"])).order_by(desc(PostingHistory.created_at)).limit(min(max(limit, 1), 100)).all()
    return [{"id": r.id, "draft_id": r.draft_id, "destination": r.destination_title, "message_id": r.message_id, "status": r.status, "detail": r.detail, "created_at": r.created_at} for r in rows]
