# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/services/publisher.py
# FUNGSI  : Pengiriman rich message ke satu tujuan
# ============================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError
from app.models import Draft, Destination, PostingHistory
from app.database import SessionLocal
from app.bot_instance import get_bot

async def publish_draft(draft_id: int, admin_id: int | None = None) -> dict:
    db = SessionLocal()
    try:
        draft = db.get(Draft, draft_id)
        if not draft:
            raise ValueError("Draft tidak ditemukan.")
        if not draft.destination_id:
            raise ValueError("Pilih satu tujuan sebelum posting.")
        destination = db.get(Destination, draft.destination_id)
        if not destination or not destination.is_active:
            raise ValueError("Tujuan tidak tersedia atau nonaktif.")
        if not (draft.text or draft.media_file_id):
            raise ValueError("Pesan belum memiliki teks atau media.")
        keyboard = [[InlineKeyboardButton(text=b["text"], url=b["url"]) for b in row] for row in (draft.buttons or [])]
        markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        bot = get_bot()
        kwargs = {"chat_id": destination.chat_id, "reply_markup": markup}
        if draft.media_type == "photo" and draft.media_file_id:
            sent = await bot.send_photo(photo=draft.media_file_id, caption=draft.text or None, parse_mode=ParseMode.HTML if draft.parse_mode == "HTML" else None, **kwargs)
        elif draft.media_type == "video" and draft.media_file_id:
            sent = await bot.send_video(video=draft.media_file_id, caption=draft.text or None, parse_mode=ParseMode.HTML if draft.parse_mode == "HTML" else None, **kwargs)
        else:
            sent = await bot.send_message(text=draft.text, parse_mode=ParseMode.HTML if draft.parse_mode == "HTML" else None, **kwargs)
        draft.status = "published"
        db.add(PostingHistory(draft_id=draft.id, admin_id=admin_id or draft.owner_id, destination_id=destination.id, destination_title=destination.title, message_id=sent.message_id, status="success", detail="Pesan berhasil dikirim."))
        db.commit()
        return {"ok": True, "message_id": sent.message_id}
    except Exception as exc:
        db.rollback()
        if 'draft' in locals() and draft:
            db.add(PostingHistory(draft_id=draft_id, admin_id=admin_id or draft.owner_id, destination_id=draft.destination_id, status="failed", detail=str(exc)[:2000]))
            db.commit()
        raise
    finally:
        db.close()
