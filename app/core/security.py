# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/core/security.py
# FUNGSI  : Dependency autentikasi dan otorisasi admin
# ============================================

from fastapi import Header, HTTPException
from app.core.telegram_auth import validate_telegram_init_data
from app.config import settings
from app.database import SessionLocal
from app.models import Admin

def current_user(x_telegram_init_data: str = Header(default="")) -> dict:
    try:
        data = validate_telegram_init_data(x_telegram_init_data)
        return data["user"]
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

def require_admin(user: dict = None, x_telegram_init_data: str = Header(default="")) -> dict:
    if user is None:
        user = current_user(x_telegram_init_data)
    uid = int(user["id"])
    db = SessionLocal()
    try:
        allowed = uid == settings.primary_admin_id or uid in settings.admins or db.get(Admin, uid) is not None
    finally:
        db.close()
    if not allowed:
        raise HTTPException(status_code=403, detail="Akses khusus admin.")
    return user
