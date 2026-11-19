from enum import Enum


class ProjectStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    RESEARCHING = "researching"
    AWAITING_BRAND_APPROVAL = "awaiting_brand_approval"
    PLANNING_PAGES = "planning_pages"
    GENERATING = "generating"
    QA = "qa"
    AWAITING_PUBLISH_APPROVAL = "awaiting_publish_approval"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
