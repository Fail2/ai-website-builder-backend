from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.app_env,
    }