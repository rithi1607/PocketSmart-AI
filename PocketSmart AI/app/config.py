from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "dev-secret-change-me"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str | None = None

    gemini_model: str = "gemini-2.5-flash"

    use_mock_ai: bool = True

    max_upload_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()