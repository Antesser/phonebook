from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        strict=False,
        case_sensitive=True,
        env_file_encoding="utf_8",
        env_file=".env_template",
        extra="ignore",
    )
    REDIS_HOST: str
    REDIS_PORT: int


def get_settings() -> Settings:
    find_dotenv()
    load_dotenv()
    return Settings()


settings = get_settings()
