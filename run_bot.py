# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : run_bot.py
# FUNGSI  : Menjalankan Telegram Bot polling
# ============================================

import logging
from telegram import (
    Update,
    WebAppInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.config import settings
from app.database import init_db

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO)
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if settings.webapp_url:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 Buka NEXORA",
                    web_app=WebAppInfo(url=settings.webapp_url)
                )
            ]
        ])

        await update.message.reply_text(
            f"Selamat datang di NEXORA RICH MESSAGE BOT, {user.first_name}!\n\n"
            "Buat, simpan, jadwalkan, dan posting rich message "
            "melalui Mini App.",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            "NEXORA aktif. Admin perlu mengatur WEBAPP_URL."
        )


async def media_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if message.photo:
        file_id = message.photo[-1].file_id
        kind = "photo"
    elif message.video:
        file_id = message.video.file_id
        kind = "video"
    else:
        return

    await message.reply_text(
        f"Jenis: {kind}\nfile_id:\n<code>{file_id}</code>",
        parse_mode="HTML"
    )


if __name__ == "__main__":
    init_db()

    app = Application.builder().token(settings.bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.PHOTO | filters.VIDEO, media_id)
    )

    app.run_polling(allowed_updates=Update.ALL_TYPES)
