from langgraph.types import interrupt

from app.core.model import get_structurer_model
from app.graph.state import WebsiteBuilderState
from app.schemas.location import LocationExtraction


def location_extraction_node(
    state: WebsiteBuilderState,
) -> dict[str, str | bool | None]:
    existing_location = state.get("location")
    if (
        state.get("location_confirmed")
        and isinstance(existing_location, str)
        and existing_location.strip()
    ):
        return {
            "location": existing_location.strip(),
            "location_confirmed": True,
            "current_stage": "planning",
        }

    prompt = state.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("A website prompt is required to extract a location.")

    model = get_structurer_model().with_structured_output(
        LocationExtraction
    )

    result = model.invoke([
        (
            "system",
            """
            Extract only the business's operating location from the user's
            website request. Do not treat a place mentioned as a destination,
            example, market, or inspiration as the business location.
            Return a location only when the request clearly states it.
            If the location is absent, ambiguous, or there are multiple
            plausible locations, return null for both fields.
            The evidence must be an exact substring copied from the user's
            request, and the location must appear within that evidence.
            Never infer or add geographic details.
            """,
        ),
        ("human", prompt),
    ])

    location = result.location.strip() if result.location else ""
    evidence = result.evidence.strip() if result.evidence else ""

    if (
        location
        and evidence
        and evidence.casefold() in prompt.casefold()
        and location.casefold() in evidence.casefold()
    ):
        return {
            "location": location,
            "location_confirmed": True,
            "current_stage": "planning",
        }

    return {
        "location": None,
        "location_confirmed": False,
        "current_stage": "location_clarification",
    }


def location_clarification_node(
    state: WebsiteBuilderState,
) -> dict[str, str | bool]:
    user_location = interrupt({
        "type": "location_clarification",
        "question": "Which city and country is this business located in?",
    })

    if not isinstance(user_location, str) or not user_location.strip():
        raise ValueError("A valid business location is required.")

    return {
        "location": user_location.strip(),
        "location_confirmed": True,
        "current_stage": "planning",
    }