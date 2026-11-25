import pytest
from pydantic import ValidationError

from app.graph.nodes import location as location_nodes
from app.graph.routers.location import route_location
from app.schemas.location import LocationExtraction


class FakeStructuredModel:
    def __init__(self, result: LocationExtraction):
        self.result = result

    def with_structured_output(self, _schema):
        return self

    def invoke(self, _messages):
        return self.result


def test_extraction_preserves_existing_confirmed_location(monkeypatch):
    def fail_if_called():
        pytest.fail("The model should not be called for a confirmed location.")

    monkeypatch.setattr(location_nodes, "get_structurer_model", fail_if_called)

    result = location_nodes.location_extraction_node({
        "location": "  Dhaka, Bangladesh  ",
        "location_confirmed": True,
    })

    assert result == {
        "location": "Dhaka, Bangladesh",
        "location_confirmed": True,
        "current_stage": "planning",
    }


def test_extraction_accepts_location_with_verbatim_prompt_evidence(monkeypatch):
    monkeypatch.setattr(
        location_nodes,
        "get_structurer_model",
        lambda: FakeStructuredModel(
            LocationExtraction(
                location="Dhaka, Bangladesh",
                evidence="Dhaka, Bangladesh",
            )
        ),
    )

    result = location_nodes.location_extraction_node({
        "prompt": "Build a website for my business in Dhaka, Bangladesh.",
    })

    assert result["location"] == "Dhaka, Bangladesh"
    assert result["location_confirmed"] is True


def test_extraction_routes_missing_location_to_clarification(monkeypatch):
    monkeypatch.setattr(
        location_nodes,
        "get_structurer_model",
        lambda: FakeStructuredModel(LocationExtraction()),
    )

    result = location_nodes.location_extraction_node({
        "prompt": "Build a website for my business.",
    })

    assert result == {
        "location": None,
        "location_confirmed": False,
        "current_stage": "location_clarification",
    }


@pytest.mark.parametrize(
    ("location", "evidence"),
    [
        ("London", "London"),
        (" ", " "),
    ],
)
def test_extraction_rejects_unverified_or_blank_location(
    monkeypatch,
    location,
    evidence,
):
    monkeypatch.setattr(
        location_nodes,
        "get_structurer_model",
        lambda: FakeStructuredModel(
            LocationExtraction(location=location, evidence=evidence)
        ),
    )

    result = location_nodes.location_extraction_node({
        "prompt": "Build a website for my business in Dhaka.",
    })

    assert result == {
        "location": None,
        "location_confirmed": False,
        "current_stage": "location_clarification",
    }


def test_extraction_requires_a_prompt(monkeypatch):
    monkeypatch.setattr(
        location_nodes,
        "get_structurer_model",
        lambda: pytest.fail("The model should not be called without a prompt."),
    )

    with pytest.raises(ValueError, match="website prompt is required"):
        location_nodes.location_extraction_node({})


def test_location_router_sends_blank_location_to_clarification():
    assert route_location({
        "location": "   ",
        "location_confirmed": True,
    }) == "location_clarification"


def test_clarification_trims_user_location(monkeypatch):
    monkeypatch.setattr(
        location_nodes,
        "interrupt",
        lambda _payload: "  Dhaka, Bangladesh  ",
    )

    result = location_nodes.location_clarification_node({})

    assert result["location"] == "Dhaka, Bangladesh"
    assert result["location_confirmed"] is True


def test_clarification_rejects_blank_user_location(monkeypatch):
    monkeypatch.setattr(
        location_nodes,
        "interrupt",
        lambda _payload: "   ",
    )

    with pytest.raises(ValueError, match="valid business location is required"):
        location_nodes.location_clarification_node({})


def test_location_extraction_rejects_extra_schema_fields():
    with pytest.raises(ValidationError):
        LocationExtraction(
            location="Dhaka",
            evidence="Dhaka",
            confidence="certain",
        )
