from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import RedisDsn, computed_field


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

    @computed_field
    @property
    def REDIS_URL(self) -> str:  # noqa
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=int(self.REDIS_PORT),
        ).unicode_string()


def get_settings() -> Settings:
    find_dotenv()
    load_dotenv()
    return Settings()


settings = get_settings()
