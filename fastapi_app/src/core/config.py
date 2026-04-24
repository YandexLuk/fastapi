from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ORIGINS: str = ""
    PORT: int = 8000
    ROOT_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr 
    AUTH_ALGORITHM: str = "HS256"

    SQLITE_URL: str = "sqlite:///sqlite.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()