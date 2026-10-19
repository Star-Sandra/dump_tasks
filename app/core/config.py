from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Dump Tasks API"
    database_url: str  # postgresql+psycopg://user:pass@host:5432/dbname
    gemini_api_key: str | None = None


settings = Settings()
