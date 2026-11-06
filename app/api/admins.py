# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/api/admins.py
# FUNGSI  : Manajemen admin oleh admin utama
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Admin
from app.schemas import AdminCreate
from app.api.deps import get_user

router = APIRouter(prefix="/api/admins", tags=["Admins"])

def primary_only(user):
    if int(user["id"]) != settings.primary_admin_id:
        raise HTTPException(403, "Hanya admin utama yang dapat mengelola admin.")

@router.get("")
def list_admins(user: dict = Depends(get_user), db: Session = Depends(get_db)):
    primary_only(user)
    return [{"user_id": a.id, "username": a.username, "is_primary": a.is_primary} for a in db.query(Admin).all()]

@router.post("")
def add_admin(payload: AdminCreate, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    primary_only(user)
    if payload.user_id == settings.primary_admin_id: raise HTTPException(400, "Admin utama sudah terdaftar.")
    item = db.get(Admin, payload.user_id) or Admin(id=payload.user_id)
    item.username = payload.username
    db.add(item); db.commit()
    return {"ok": True, "user_id": item.id}

@router.delete("/{user_id}")
def remove_admin(user_id: int, user: dict = Depends(get_user), db: Session = Depends(get_db)):
    primary_only(user)
    if user_id == settings.primary_admin_id: raise HTTPException(400, "Admin utama tidak dapat dihapus.")
    item = db.get(Admin, user_id)
    if not item: raise HTTPException(404, "Admin tidak ditemukan.")
    db.delete(item); db.commit()
    return {"ok": True}
