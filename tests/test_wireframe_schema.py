import pytest
from pydantic import ValidationError

from app.schemas.wireframe import (
    CallToAction,
    NavigationItem,
    PageWireframe,
    WireframeOutput,
    WireframeSection,
)


def make_page(slug="home"):
    return PageWireframe(
        page_name="Home",
        page_slug=slug,
        page_purpose="Introduce the business and convert relevant visitors.",
        audience_need="Understand the services and decide whether to contact the business.",
        seo_focus=["business services"],
        sections=[
            WireframeSection(
                section_id="hero",
                title="Hero",
                purpose="Communicate the main value proposition.",
                layout_description="A two-column layout with text and supporting visual.",
                content_requirements=["Headline", "Supporting summary"],
                recommended_components=["Heading", "Button", "Image"],
            )
        ],
        primary_cta=CallToAction(
            label="Contact us",
            action="Open the contact form.",
        ),
    )


def test_wireframe_requires_homepage():
    with pytest.raises(ValidationError, match="homepage"):
        WireframeOutput(
            website_goal="Generate qualified enquiries for the business.",
            navigation=[NavigationItem(label="Services", page_slug="services")],
            pages=[
                make_page("services"),
            ],
            global_functional_requirements=["Responsive navigation"],
        )


def test_wireframe_rejects_duplicate_page_slugs():
    with pytest.raises(ValidationError, match="unique"):
        WireframeOutput(
            website_goal="Generate qualified enquiries for the business.",
            navigation=[NavigationItem(label="Home", page_slug="home")],
            pages=[make_page(), make_page()],
            global_functional_requirements=["Responsive navigation"],
        )


def test_wireframe_rejects_navigation_to_unknown_page():
    with pytest.raises(ValidationError, match="unknown pages"):
        WireframeOutput(
            website_goal="Generate qualified enquiries for the business.",
            navigation=[NavigationItem(label="About", page_slug="about")],
            pages=[make_page()],
            global_functional_requirements=["Responsive navigation"],
        )


def test_wireframe_accepts_valid_homepage_and_navigation():
    result = WireframeOutput(
        website_goal="Generate qualified enquiries for the business.",
        navigation=[NavigationItem(label="Home", page_slug="home")],
        pages=[make_page()],
        global_functional_requirements=["Responsive navigation"],
    )

    assert result.pages[0].page_slug == "home"
