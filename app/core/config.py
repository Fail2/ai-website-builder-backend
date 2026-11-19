from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    app_name: str = "AI Website Builder"
    app_env: str = "development"
    debug: bool = True

    database_url: str = (
        "postgresql+asyncpg://postgres:local_dev_password_123@localhost:5432/ai_website_builder"
    )

    model_provider: str = "openai"
    model_name: str = "openai/gpt-oss-120b"
    model_api_key: SecretStr | None = None
    model_base_url: str = "https://api.groq.com/openai/v1"

    tavily_api_key: SecretStr | None = None
    firecrawl_api_key: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
