# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/api/drafts.py
# FUNGSI  : Pembuatan, penyimpanan, dan posting draft
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Draft, Destination
from app.schemas import DraftCreate
from app.api.deps import get_user
from app.core.security import require_admin
from app.services.publisher import publish_draft

router = APIRouter(prefix="/api/drafts", tags=["Drafts"])

def serialize(d):
    return {"id": d.id, "title": d.title, "text": d.text, "media_type": d.media_type, "media_file_id": d.media_file_id, "parse_mode": d.parse_mode, "buttons": d.buttons or [], "destination_id": d.destination_id, "scheduled_at": d.scheduled_at, "status": d.status}

@router.get("")
def list_drafts(user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    return [serialize(d) for d in db.query(Draft).order_by(Draft.updated_at.desc()).all()]

@router.post("")
def create_draft(payload: DraftCreate, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    if payload.destination_id and not db.get(Destination, payload.destination_id): raise HTTPException(404, "Tujuan tidak ditemukan.")
    data = payload.model_dump()
    item = Draft(owner_id=int(user["id"]), status="scheduled" if data.get("scheduled_at") else "draft", **data)
    db.add(item); db.commit(); db.refresh(item)
    return serialize(item)

@router.put("/{draft_id}")
def update_draft(draft_id: int, payload: DraftCreate, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    item = db.get(Draft, draft_id)
    if not item: raise HTTPException(404, "Draft tidak ditemukan.")
    data = payload.model_dump()
    for key, value in data.items(): setattr(item, key, value)
    item.status = "scheduled" if item.scheduled_at else "draft"
    db.commit(); db.refresh(item)
    return serialize(item)

@router.delete("/{draft_id}")
def delete_draft(draft_id: int, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    item = db.get(Draft, draft_id)
    if not item: raise HTTPException(404, "Draft tidak ditemukan.")
    db.delete(item); db.commit()
    return {"ok": True}

@router.post("/{draft_id}/publish")
async def publish(draft_id: int, user: dict = Depends(get_user)):
    require_admin(user)
    try: return await publish_draft(draft_id, int(user["id"]))
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc
    except Exception as exc: raise HTTPException(502, f"Gagal mengirim pesan: {exc}") from exc
