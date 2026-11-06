# ============================================
# PROJECT : NEXORA RICH MESSAGE BOT
# FILE    : app/config.py
# FUNGSI  : Memuat konfigurasi environment
# ============================================

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    bot_username: str = ""
    database_url: str
    webapp_url: str = ""
    app_secret: str
    admin_ids: str = ""
    primary_admin_id: int
    telegram_init_data_max_age: int = 86400
    timezone: str = "Asia/Jakarta"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def admins(self) -> set[int]:
        return {int(x.strip()) for x in self.admin_ids.split(",") if x.strip().isdigit()}

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
