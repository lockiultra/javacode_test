from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent.parent
ENV_PATH = BASE_DIR / '.env'


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding='utf-8')


print(ENV_PATH)
settings = Settings()
