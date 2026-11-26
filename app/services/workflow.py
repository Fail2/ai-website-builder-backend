from uuid import UUID

from sqlalchemy import select

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


async def run_website_workflow(
    graph,
    project_id: UUID,
    initial_state: dict,
):
    try:
        result = await graph.ainvoke(
            initial_state,
            config={
                "configurable": {
                    "thread_id": str(project_id),
                }
            },
        )

        interrupts = result.get("__interrupt__", [])

        if interrupts:
            interrupt_type = interrupts[0].value.get("type")

            if interrupt_type == "brand_guideline_review":
                await update_project_status(
                    project_id,
                    ProjectStatus.AWAITING_BRAND_APPROVAL,
                )
            else:
                await update_project_status(
                    project_id,
                    ProjectStatus.PLANNING,
                )

        else:
            # Current graph ends after brand approval.
            # Wireframe workflow will be connected later.
            await update_project_status(
                project_id,
                ProjectStatus.PLANNING_PAGES,
            )

    except Exception:
        await update_project_status(
            project_id,
            ProjectStatus.FAILED,
        )
        raise