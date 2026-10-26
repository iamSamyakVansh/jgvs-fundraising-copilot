"""Shared application configuration and design tokens."""
from enum import StrEnum

APP_TITLE = "JGVS Fundraising Copilot"
PERSISTENCE_ENABLED = False

COLORS = {
    "ink": "#1d1d1f",
    "muted": "#515154",
    "accent": "#0071e3",
    "accent_hover": "#0062c4",
    "paper": "#f5f5f7",
    "line": "#d2d2d7",
    "white": "#ffffff",
}


class Stage(StrEnum):
    RESEARCH = "Research"
    QUALIFIED = "Qualified"
    DRAFTING = "Drafting"
    SUBMITTED = "Submitted"
    AWARDED = "Awarded"
    DECLINED = "Declined"
    ON_HOLD = "On hold"


class OpportunityStatus(StrEnum):
    NEEDS_VERIFICATION = "Needs verification"
    RESEARCH_COMPLETE = "Research complete"


class ApprovalStatus(StrEnum):
    PENDING = "Pending human review"
    APPROVED = "Approved"
    CHANGES_REQUESTED = "Changes requested"


STAGES = [stage.value for stage in Stage]
