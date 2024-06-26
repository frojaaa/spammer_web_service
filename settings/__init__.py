from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = 'localhost'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')


BASE_DIR = Path(__file__).parent.parent.resolve()
