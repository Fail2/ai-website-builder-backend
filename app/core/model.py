from functools import lru_cache

from langchain.chat_models import init_chat_model

from app.core.config import settings


@lru_cache(maxsize=1)
def get_model():
    if settings.model_api_key is None:
        raise ValueError("MODEL_API_KEY is not configured")

    return init_chat_model(
        model=settings.model_name,
        model_provider=settings.model_provider,
        api_key=settings.model_api_key.get_secret_value(),
        base_url=settings.model_base_url,
        temperature=0,
    )