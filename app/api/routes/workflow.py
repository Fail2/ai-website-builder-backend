import asyncio
import json
from uuid import UUID

from fastapi import APIRouter, Request
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
                    f"event: {event_type}\n"
                    f"data: {json.dumps(event, default=str)}\n\n"
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