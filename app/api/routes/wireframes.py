from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from app.schemas.wireframe_review import WireframeReviewRequest
from app.services.workflow import resume_website_workflow


router = APIRouter(prefix="/api/projects", tags=["Wireframes"])


@router.post(
    "/{project_id}/wireframe-review",
    status_code=status.HTTP_202_ACCEPTED,
)
async def review_wireframe(
    project_id: UUID,
    payload: WireframeReviewRequest,
    request: Request,
    background_tasks: BackgroundTasks,
):
    graph = request.app.state.website_builder_graph
    config = {"configurable": {"thread_id": str(project_id)}}
    snapshot = await graph.aget_state(config)

    pending_interrupts = [
        interrupt
        for task in snapshot.tasks
        for interrupt in task.interrupts
    ]
    is_waiting_for_wireframe = any(
        item.value.get("type") == "wireframe_review"
        for item in pending_interrupts
    )
    if not is_waiting_for_wireframe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workflow is not waiting for wireframe review.",
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
        "message": "Wireframe review received. Workflow resumption started.",
    }
