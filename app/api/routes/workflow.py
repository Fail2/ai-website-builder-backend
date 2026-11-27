import asyncio
import json
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    Request,
    status,
)

from app.schemas.location import LocationResumeRequest
from app.services.workflow import resume_website_workflow
from app.services.event_hub import event_hub
from fastapi.responses import StreamingResponse

from app.services.event_hub import event_hub


router = APIRouter(
    prefix="/api/projects",
    tags=["Workflow"],
)


@router.get("/{project_id}/events")
async def stream_project_events(
    project_id: UUID,
    request: Request,
):
    async def event_generator():
        queue = await event_hub.subscribe(project_id)

        while True:
            # Stop streaming if client disconnects
            if await request.is_disconnected():
                break

            try:
                event = await asyncio.wait_for(
                    queue.get(),
                    timeout=15,
                )

                event_type = event.get("type", "message")

                yield (
                    f"event: {event_type}\ndata: {json.dumps(event, default=str)}\n\n"
                )

                # Stop stream on terminal events
                if event_type in ("completed", "error"):
                    break

            except asyncio.TimeoutError:
                # Keep SSE connection alive
                yield ": heartbeat\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/{project_id}/location", status_code=status.HTTP_202_ACCEPTED)
async def submit_location(
    project_id: UUID,
    payload: LocationResumeRequest,
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

    # Verify that the graph is waiting for location input.
    pending_interrupts = [
        interrupt for task in snapshot.tasks for interrupt in task.interrupts
    ]

    location_interrupt = next(
        (
            item
            for item in pending_interrupts
            if item.value.get("type") == "location_clarification"
        ),
        None,
    )

    if location_interrupt is None:
        raise HTTPException(
            status_code=409,
            detail="Workflow is not waiting for location input.",
        )

    location = payload.location.strip()

    if not location:
        raise HTTPException(
            status_code=422,
            detail="Location cannot be empty.",
        )

    # Initialize/subscribe before resuming so events are not missed.
    await event_hub.subscribe(project_id)

    background_tasks.add_task(
        resume_website_workflow,
        graph,
        project_id,
        location,
    )

    return {
        "message": "Location received. Workflow resumption started.",
        "project_id": str(project_id),
        "location": location,
        "status": "resuming",
    }
