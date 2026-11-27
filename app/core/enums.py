from enum import Enum


class ProjectStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    RESEARCHING = "researching"
    AWAITING_LOCATION = "awaiting_location"
    AWAITING_BRAND_APPROVAL = "awaiting_brand_approval"
    PLANNING_PAGES = "planning_pages"
    AWAITING_PAGE_CONFIRMATION = "awaiting_page_confirmation"
    GENERATING = "generating"
    AWAITING_PUBLISH_APPROVAL = "awaiting_publish_approval"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
