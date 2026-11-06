# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/bot_instance.py
# FUNGSI  : Instance Telegram Bot bersama
# ============================================

from telegram import Bot
from app.config import settings

_bot = Bot(settings.bot_token)
def get_bot() -> Bot:
    return _bot
