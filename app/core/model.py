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

@lru_cache(maxsize=1)
def get_structurer_model():
    if settings.structurer_model_api_key is None:
        raise ValueError("STRUCTURER_MODEL_API_KEY is not configured")

    return init_chat_model(
        model=settings.structurer_model_name,
        model_provider=settings.structurer_model_provider,
        api_key=settings.structurer_model_api_key.get_secret_value(),
        base_url=settings.structurer_model_base_url,
        temperature=0,
    )

@lru_cache(maxsize=1)
def get_brand_model():
    if settings.brand_model_api_key is None:
        raise ValueError("BRAND_MODEL_API_KEY is not configured")

    return init_chat_model(
        model=settings.brand_model_name,
        model_provider=settings.brand_model_provider,
        api_key=settings.brand_model_api_key.get_secret_value(),
        base_url=settings.brand_model_base_url,
        temperature=0,
    )