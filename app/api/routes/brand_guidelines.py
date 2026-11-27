from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from app.schemas.brand_guideline_review import BrandGuidelineReviewRequest
from app.services.workflow import resume_website_workflow


router = APIRouter(
    prefix="/api/projects",
    tags=["Brand Guidelines"],
)


@router.post(
    "/{project_id}/brand-guideline-review",
    status_code=status.HTTP_202_ACCEPTED,
)
async def review_brand_guideline(
    project_id: UUID,
    payload: BrandGuidelineReviewRequest,
    request: Request,
    background_tasks: BackgroundTasks,
):
    graph = request.app.state.website_builder_graph

    config = {
        "configurable": {
            "thread_id": str(project_id),
        }
    }

    snapshot = await graph.aget_state(config)

    pending_interrupts = [
        interrupt
        for task in snapshot.tasks
        for interrupt in task.interrupts
    ]

    is_waiting_for_brand_review = any(
        item.value.get("type") == "brand_guideline_review"
        for item in pending_interrupts
    )

    if not is_waiting_for_brand_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workflow is not waiting for brand guideline review.",
        )

    decision = payload.model_dump(exclude_none=True)

    background_tasks.add_task(
        resume_website_workflow,
        graph,
        project_id,
        decision,
    )

    return {
        "project_id": str(project_id),
        "status": "resuming",
        "message": "Brand guideline review received. Workflow resumption started.",
    }