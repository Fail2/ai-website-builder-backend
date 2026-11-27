from pydantic import BaseModel, ConfigDict, Field, model_validator


class CallToAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(min_length=2, max_length=60)
    action: str = Field(
        min_length=5,
        max_length=160,
        description="What happens when the visitor activates this CTA.",
    )


class NavigationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(min_length=2, max_length=40)
    page_slug: str = Field(
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="Slug of a page included in the pages list.",
    )


class WireframeSection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    title: str = Field(min_length=2, max_length=80)
    purpose: str = Field(min_length=10, max_length=240)
    layout_description: str = Field(min_length=10, max_length=400)
    content_requirements: list[str] = Field(min_length=1, max_length=8)
    recommended_components: list[str] = Field(min_length=1, max_length=8)


class PageWireframe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_name: str = Field(min_length=2, max_length=60)
    page_slug: str = Field(
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="Use 'home' for the homepage.",
    )
    page_purpose: str = Field(min_length=10, max_length=300)
    audience_need: str = Field(min_length=10, max_length=240)
    seo_focus: list[str] = Field(min_length=1, max_length=8)
    sections: list[WireframeSection] = Field(min_length=1, max_length=15)
    primary_cta: CallToAction
    secondary_cta: CallToAction | None = None

    @model_validator(mode="after")
    def validate_section_ids(self):
        section_ids = [section.section_id for section in self.sections]
        if len(section_ids) != len(set(section_ids)):
            raise ValueError("Section IDs must be unique within a page.")
        return self


class WireframeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    website_goal: str = Field(min_length=20, max_length=400)
    navigation: list[NavigationItem] = Field(min_length=1, max_length=8)
    pages: list[PageWireframe] = Field(min_length=1, max_length=10)
    global_functional_requirements: list[str] = Field(
        min_length=1,
        max_length=12,
    )

    @model_validator(mode="after")
    def validate_page_structure(self):
        page_slugs = [page.page_slug for page in self.pages]
        if len(page_slugs) != len(set(page_slugs)):
            raise ValueError("Page slugs must be unique.")

        if "home" not in page_slugs:
            raise ValueError("A homepage with page_slug='home' is required.")

        navigation_slugs = [item.page_slug for item in self.navigation]
        if len(navigation_slugs) != len(set(navigation_slugs)):
            raise ValueError("Navigation page slugs must be unique.")

        unknown_pages = set(navigation_slugs) - set(page_slugs)
        if unknown_pages:
            raise ValueError(
                f"Navigation references unknown pages: {sorted(unknown_pages)}"
            )

        return self
