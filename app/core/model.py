from functools import lru_cache

from langchain.chat_models import init_chat_model

from app.core.config import settings


def create_model(model: str, api_key: str):
    if api_key is None:
            raise ValueError("API_KEY is not configured")
    
    return init_chat_model(
        model=model,
        api_key=api_key,
        max_retries=5,
    )


@lru_cache(maxsize=1)
def get_structurer_model():
     return create_model(settings.structurer_model_name, settings.structurer_model_api_key)

@lru_cache(maxsize=1)
def get_brand_model():
      return create_model(settings.brand_model_name, settings.brand_model_api_key)