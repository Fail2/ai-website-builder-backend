from uuid import UUID

from sqlalchemy import select
from langgraph.types import Command

from app.services.event_hub import event_hub
from app.core.enums import ProjectStatus
from app.database.session import AsyncSessionLocal
from app.models.project import Project


async def update_project_status(
    project_id: UUID,
    status: ProjectStatus,
):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if project is None:
            return

        project.status = status
        await db.commit()


async def run_website_workflow(graph, project_id, initial_state):
    config = {
        "configurable": {
            "thread_id": str(project_id)
        },
        "max_concurrency": 2,
    }

    try:
        async for chunk in graph.astream(
            initial_state,
            config=config,
            stream_mode="updates",
        ):
            for node_name, update in chunk.items():

                if node_name == "__interrupt__":
                    for interrupt in update:
                        await event_hub.publish(
                            project_id,
                            {
                                "type": "interrupt",
                                "data": interrupt.value,
                            },
                        )
                    continue

                await event_hub.publish(
                    project_id,
                    {
                        "type": "node_update",
                        "node": node_name,
                        "data": update,
                    },
                )

        await event_hub.publish(
            project_id,
            {"type": "completed"},
        )

    except Exception as exc:
        await event_hub.publish(
            project_id,
            {
                "type": "error",
                "message": str(exc),
            },
        )
        raise


async def resume_website_workflow(graph, project_id, location: str,):
    config = {
        "configurable": {
            "thread_id": str(project_id),
        },
        "max_concurrency": 2,
    }

    async for chunk in graph.astream(
        Command(resume=location),
        config=config,
        stream_mode="updates",
    ):
        interrupts = chunk.get("__interrupt__")

        if interrupts:
            for item in interrupts:
                await event_hub.publish(
                    project_id,
                    {
                        "type": "interrupt",
                        "data": item.value,
                    },
                )
            return

        for node_name, update in chunk.items():
            await event_hub.publish(
                project_id,
                {
                    "type": "node_update",
                    "node": node_name,
                    "data": update,
                },
            )

    await event_hub.publish(
        project_id,
        {"type": "completed"},
    )