# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/schemas.py
# FUNGSI  : Skema validasi request API
# ============================================

from datetime import datetime
from pydantic import BaseModel, Field

class DestinationCreate(BaseModel):
    chat_id: int
    title: str = Field(min_length=1, max_length=200)
    chat_type: str = "channel"

class DraftCreate(BaseModel):
    title: str = "Draft"
    text: str = ""
    media_type: str | None = None
    media_file_id: str | None = None
    parse_mode: str = "HTML"
    buttons: list[list[dict[str, str]]] = []
    destination_id: int | None = None
    scheduled_at: datetime | None = None

class AdminCreate(BaseModel):
    user_id: int
    username: str | None = None
