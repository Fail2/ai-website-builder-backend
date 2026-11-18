import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreate, ProjectStatus


def test_valid_project_creation():
    project = ProjectCreate(
        brand_name="TravelMate",
        prompt="Build a travel booking website.",
        niche="Travel",
    )

    assert project.brand_name == "TravelMate"
    assert project.niche == "Travel"


def test_project_creation_rejects_missing_fields():
    with pytest.raises(ValidationError):
        ProjectCreate(
            brand_name="TravelMate",
            prompt="Build a travel booking website.",
        )


def test_project_creation_rejects_extra_fields():
    with pytest.raises(ValidationError):
        ProjectCreate(
            brand_name="TravelMate",
            prompt="Build a travel booking website.",
            niche="Travel",
            user_id="123",
        )


def test_project_status_values():
    assert ProjectStatus.CREATED.value == "created"
    assert ProjectStatus.COMPLETED.value == "completed"
