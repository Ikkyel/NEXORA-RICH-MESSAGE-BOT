# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/core/telegram_auth.py
# FUNGSI  : Validasi autentikasi Telegram Mini App
# ============================================

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from app.config import settings

def validate_telegram_init_data(init_data: str) -> dict:
    if not init_data:
        raise ValueError("Init data kosong.")
    values = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = values.pop("hash", None)
    if not received_hash:
        raise ValueError("Hash autentikasi tidak ditemukan.")
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(values.items()))
    secret = hmac.new(b"WebAppData", settings.bot_token.encode(), hashlib.sha256).digest()
    expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        raise ValueError("Hash autentikasi tidak valid.")
    auth_date = int(values.get("auth_date", "0"))
    now = int(time.time())
    if auth_date <= 0 or auth_date > now or now - auth_date > settings.telegram_init_data_max_age:
        raise ValueError("Sesi Telegram tidak valid atau kedaluwarsa.")
    try:
        user = json.loads(values["user"])
    except (KeyError, json.JSONDecodeError) as exc:
        raise ValueError("Data pengguna Telegram tidak valid.") from exc
    if not isinstance(user, dict) or not user.get("id"):
        raise ValueError("ID pengguna Telegram tidak ditemukan.")
    values["user"] = user
    return values
