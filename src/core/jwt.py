from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class SettingsJWT(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # JWT_KEY is kept as the primary name to stay compatible with the existing .env.local
    SECRET_KEY: str = Field(validation_alias=AliasChoices("JWT_KEY", "SECRET_KEY"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Single admin, no accounts table: credentials live in the environment
    ADMIN_LOGIN: str = Field(validation_alias=AliasChoices("ADMIN_LOGIN", "ADMIN_USERNAME"))
    ADMIN_PASSWORD: str


settings_jwt = SettingsJWT()
