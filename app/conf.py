from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str | None = None
    DB_PASSWORD: str | None = None
    DB_USER: str | None = None
    DB_NAME: str | None = None
    DB_PORT: int | None = None

    @property
    def get_url_sqlite(self):
        return f"sqlite:///ecommerce.db"

    @property
    def get_url_postgres(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

    @property
    def get_url_async_postgres(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()