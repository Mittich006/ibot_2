from subprocess import run
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # .env configuration.
    class Config:
        env_file = Path('./.env').resolve(True)

    # .env file vars.
    TELEGRAM_BOT_API_KEY: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PGDATA: str

    COMPYSHOPDB_URL: str = ''

settings = Settings()

# Database URLs configuartion.
settings.COMPYSHOPDB_URL:str = f"postgresql+asyncpg://"+\
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@" +\
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_HOST}"

