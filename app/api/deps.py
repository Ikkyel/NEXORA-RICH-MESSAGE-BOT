# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/api/deps.py
# FUNGSI  : Dependency autentikasi API
# ============================================

from fastapi import Header, HTTPException
from app.core.telegram_auth import validate_telegram_init_data

def get_user(x_telegram_init_data: str = Header(default="")) -> dict:
    try:
        return validate_telegram_init_data(x_telegram_init_data)["user"]
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
