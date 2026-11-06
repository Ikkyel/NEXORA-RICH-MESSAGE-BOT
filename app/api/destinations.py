# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/api/destinations.py
# FUNGSI  : Manajemen channel dan grup tujuan
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Destination
from app.schemas import DestinationCreate
from app.api.deps import get_user
from app.core.security import require_admin

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@router.get("")
def list_destinations(user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    return [{"id": d.id, "chat_id": d.chat_id, "title": d.title, "chat_type": d.chat_type, "is_active": d.is_active} for d in db.query(Destination).order_by(Destination.title).all()]

@router.post("")
def add_destination(payload: DestinationCreate, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    item = db.query(Destination).filter_by(chat_id=payload.chat_id).first()
    if item:
        item.title, item.chat_type, item.is_active = payload.title, payload.chat_type, True
    else:
        item = Destination(**payload.model_dump())
        db.add(item)
    db.commit(); db.refresh(item)
    return {"id": item.id, "title": item.title, "chat_id": item.chat_id}

@router.delete("/{destination_id}")
def delete_destination(destination_id: int, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    require_admin(user)
    item = db.get(Destination, destination_id)
    if not item: raise HTTPException(404, "Tujuan tidak ditemukan.")
    item.is_active = False
    db.commit()
    return {"ok": True}
