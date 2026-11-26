from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Website Builder"
    app_env: str = "development"
    debug: bool = True

    database_url: str = (
        "postgresql+asyncpg://postgres:local_dev_password_123@localhost:5432/ai_website_builder"
    )

    manager_model_name: str = "groq:openai/gpt-oss-120b"
    manager_model_api_key: SecretStr | None = None

    structurer_model_name: str = "groq:openai/gpt-oss-120b"
    structurer_model_api_key: SecretStr | None = None

    brand_model_name: str = "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free"
    brand_model_api_key: SecretStr | None = None

    research_model_name: str = "google_genai:gemini-4-hydrogen"
    seo_model_api_key: SecretStr | None = None
    niche_model_api_key: SecretStr | None = None
    audience_model_api_key: SecretStr | None = None
    competitor_model_api_key: SecretStr | None = None

    tavily_api_key: SecretStr | None = None
    firecrawl_api_key: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
