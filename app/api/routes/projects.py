from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

from fastapi import BackgroundTasks, Request
from app.core.enums import ProjectStatus
from app.services.workflow import run_website_workflow

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    project = Project(
        brand_name=payload.brand_name,
        prompt=payload.prompt,
        niche=payload.niche,
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.post(
    "/{project_id}/generate",
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_website(
    project_id: UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .with_for_update()
    )

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    if project.status != ProjectStatus.CREATED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project generation has already started.",
        )

    initial_state = {
        "project_id": str(project.id),
        "brand_name": project.brand_name,
        "prompt": project.prompt,
        "niche": project.niche,
        "current_stage": "location_extraction",
        "location_confirmed": False,
    }

    project.status = ProjectStatus.PLANNING
    await db.commit()

    background_tasks.add_task(
        run_website_workflow,
        request.app.state.website_builder_graph,
        project.id,
        initial_state,
    )

    return {
        "project_id": str(project.id),
        "status": ProjectStatus.PLANNING.value,
        "message": "Website generation started.",
    }