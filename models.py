"""Typed domain models used by the demo workspace."""
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any

from config import ApprovalStatus, OpportunityStatus, Stage
from services.ids import new_id


@dataclass
class Opportunity:
    donor: str
    title: str
    theme: str
    geography: str
    amount: str
    deadline: str
    eligibility: str
    source: str
    status: str = OpportunityStatus.NEEDS_VERIFICATION
    id: str = field(default_factory=new_id)
    illustrative: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Donor:
    donor: str
    contact: str = "Not supplied"
    email: str = "Information Required"
    opportunity: str = "—"
    stage: str = Stage.RESEARCH
    amount: str = "Information Required"
    next_action: str = "Verify source and eligibility"
    notes: str = ""
    interactions: list[dict[str, str]] = field(default_factory=list)
    id: str = field(default_factory=new_id)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ApprovalItem:
    item_type: str
    item: str
    content: str = ""
    status: str = ApprovalStatus.PENDING
    created: str = field(default_factory=lambda: date.today().isoformat())
    id: str = field(default_factory=new_id)
    version: int = 1
    reviewer_comment: str = ""
    audit: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OrgProfile:
    name: str = "Jan Gramin Vikash Sansthan (JGVS)"
    focus: list[str] = field(default_factory=lambda: ["Information Required"])
    registration: str = "Information Required"
    tax_status: str = "Information Required"
    csr1: str = "Information Required"
    annual_budget: str = "Information Required"
    beneficiaries: str = "Information Required"
    facts: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
