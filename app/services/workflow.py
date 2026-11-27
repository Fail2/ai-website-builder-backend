from uuid import UUID

from langgraph.types import Command
from sqlalchemy import select

from app.core.enums import ProjectStatus
from app.database.session import AsyncSessionLocal
from app.models.project import Project
from app.services.event_hub import event_hub


INTERRUPT_STATUSES = {
    "location_clarification": ProjectStatus.AWAITING_LOCATION,
    "brand_guideline_review": ProjectStatus.AWAITING_BRAND_APPROVAL,
    "wireframe_review": ProjectStatus.AWAITING_PAGE_CONFIRMATION,
}


async def update_project_status(project_id: UUID, status: ProjectStatus) -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        if project is None:
            return
        project.status = status
        await db.commit()


async def _stream_graph(graph, project_id: UUID, input_value) -> None:
    config = {
        "configurable": {"thread_id": str(project_id)},
        "max_concurrency": 2,
    }

    async for chunk in graph.astream(
        input_value,
        config=config,
        stream_mode="updates",
    ):
        for node_name, update in chunk.items():
            if node_name == "__interrupt__":
                # Interrupts are published after the stream using the checkpoint,
                # so they can be handled consistently across LangGraph versions.
                continue
            await event_hub.publish(
                project_id,
                {
                    "type": "node_update",
                    "node": node_name,
                    "data": update,
                },
            )

    snapshot = await graph.aget_state(config)
    pending_interrupts = [
        interrupt
        for task in snapshot.tasks
        for interrupt in task.interrupts
    ]

    if pending_interrupts:
        for interrupt in pending_interrupts:
            interrupt_type = interrupt.value.get("type")
            status = INTERRUPT_STATUSES.get(interrupt_type)
            if status is not None:
                await update_project_status(project_id, status)
            await event_hub.publish(
                project_id,
                {
                    "type": "interrupt",
                    "data": interrupt.value,
                },
            )
        return

    await event_hub.publish(project_id, {"type": "completed"})


async def run_website_workflow(graph, project_id: UUID, initial_state: dict) -> None:
    try:
        await _stream_graph(graph, project_id, initial_state)
    except Exception as exc:
        await update_project_status(project_id, ProjectStatus.FAILED)
        await event_hub.publish(
            project_id,
            {"type": "error", "message": str(exc)},
        )
        raise


async def resume_website_workflow(
    graph,
    project_id: UUID,
    decision: dict | str,
) -> None:
    try:
        await _stream_graph(
            graph,
            project_id,
            Command(resume=decision),
        )
    except Exception as exc:
        await update_project_status(project_id, ProjectStatus.FAILED)
        await event_hub.publish(
            project_id,
            {"type": "error", "message": str(exc)},
        )
        raise
