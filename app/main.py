from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.engine import make_url

from app.api.routes.projects import router as projects_router
from app.api.routes.workflow import router as workflow_router
from app.core.config import settings
from app.graph.builder import compile_website_builder_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = make_url(settings.database_url)

    checkpoint_url = database_url.set(
        drivername="postgresql"
    ).render_as_string(hide_password=False)

    async with AsyncPostgresSaver.from_conn_string(checkpoint_url) as checkpointer:
        await checkpointer.setup()

        app.state.website_builder_graph = (compile_website_builder_graph(checkpointer))

        yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(projects_router)
app.include_router(workflow_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.app_env,
    }