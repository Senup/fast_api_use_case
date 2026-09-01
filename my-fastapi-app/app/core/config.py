from pydantic_settings import BaseSettings, SettingsConfigDict
# copmments missing

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "FastAPI Learning Lab"
    app_version: str = "0.1.0"
    debug: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()