# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/models.py
# FUNGSI  : Model tabel database PostgreSQL
# ============================================

from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Destination(Base):
    __tablename__ = "destinations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    chat_type: Mapped[str] = mapped_column(String(30), default="channel")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Draft(Base):
    __tablename__ = "drafts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), default="Draft")
    text: Mapped[str] = mapped_column(Text, default="")
    media_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    media_file_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    parse_mode: Mapped[str] = mapped_column(String(20), default="HTML")
    buttons: Mapped[list] = mapped_column(JSON, default=list)
    destination_id: Mapped[int | None] = mapped_column(ForeignKey("destinations.id", ondelete="SET NULL"), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class PostingHistory(Base):
    __tablename__ = "posting_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    draft_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    destination_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    destination_title: Mapped[str] = mapped_column(String(200), default="")
    message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
