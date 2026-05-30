from pathlib import Path
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    secret_key: str = "changeme_use_32_random_chars_here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite+aiosqlite:///./language_converter.db"
    frontend_url: str = "http://localhost:3000"

    model_config = {"env_file": str(ENV_FILE), "extra": "ignore"}


settings = Settings()
