from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_password: str
    database_name: str
    database_user: str
    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
        )

settings = Settings()