from langchain.chat_models import init_chat_model

from app.core.config import settings


def get_model():
    return init_chat_model(
        model=settings.model_name,
        model_provider=settings.model_provider,
        api_key=settings.model_api_key.get_secret_value(),
        base_url=settings.model_base_url,
        temperature=0,
    )