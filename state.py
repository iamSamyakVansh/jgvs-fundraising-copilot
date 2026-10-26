"""Centralized session-state initialization and typed accessors."""
from typing import Any

import streamlit as st

from config import PERSISTENCE_ENABLED
from data.repository import SQLiteRepository
from data.seed import donors, opportunities, org_profile
from models import ApprovalItem, Donor, Opportunity, OrgProfile

STATE_OPPORTUNITIES = "opportunities"
STATE_DONORS = "donors"
STATE_APPROVALS = "approvals"
STATE_ORG = "org_profile"


def _repository() -> SQLiteRepository | None:
    """Get optional persistence adapter when explicitly enabled."""
    return SQLiteRepository() if PERSISTENCE_ENABLED else None


def persist(key: str) -> None:
    """Write a session value to the optional repository when enabled."""
    repository = _repository()
    if repository:
        repository.save(key, st.session_state[key])


def init_state() -> None:
    """Initialize app state once; session-only mode is the default."""
    repository = _repository()
    defaults: dict[str, Any] = {
        STATE_OPPORTUNITIES: [item.to_dict() for item in opportunities()],
        STATE_DONORS: [item.to_dict() for item in donors()],
        STATE_APPROVALS: [],
        STATE_ORG: org_profile().to_dict(),
        "eligibility_checks": {},
        "documents": [],
        "followups": [],
        "proposal_versions": [],
        "audit_user": "Demo reviewer",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            stored = repository.load(key) if repository else None
            st.session_state[key] = stored if stored is not None else default


def get_opportunities() -> list[dict[str, Any]]:
    """Return typed opportunity dictionaries from session state."""
    return st.session_state[STATE_OPPORTUNITIES]


def set_opportunities(items: list[dict[str, Any]]) -> None:
    """Replace opportunities and persist when SQLite mode is enabled."""
    st.session_state[STATE_OPPORTUNITIES] = items
    repository = _repository()
    if repository:
        repository.save(STATE_OPPORTUNITIES, items)


def get_donors() -> list[dict[str, Any]]:
    """Return donor rows from session state."""
    return st.session_state[STATE_DONORS]


def get_approvals() -> list[dict[str, Any]]:
    """Return human-review queue records."""
    return st.session_state[STATE_APPROVALS]


def set_approvals(items: list[dict[str, Any]]) -> None:
    """Replace review records and persist when configured."""
    st.session_state[STATE_APPROVALS] = items
    persist(STATE_APPROVALS)


def get_followups() -> list[dict[str, Any]]:
    """Return reminder records."""
    return st.session_state["followups"]


def add_followup(item: dict[str, Any]) -> None:
    """Append a reminder and persist when enabled."""
    get_followups().append(item)
    persist("followups")


def get_proposal_versions() -> list[dict[str, Any]]:
    """Return versioned proposal drafts."""
    return st.session_state["proposal_versions"]


def add_proposal_version(item: dict[str, Any]) -> None:
    """Append a proposal version and persist when enabled."""
    get_proposal_versions().append(item)
    persist("proposal_versions")


def get_eligibility_checks(opportunity_id: str) -> list[str]:
    """Return saved checklist labels for one opportunity."""
    return st.session_state["eligibility_checks"].setdefault(opportunity_id, [])


def set_eligibility_checks(opportunity_id: str, labels: list[str]) -> None:
    """Save checklist labels for one opportunity."""
    st.session_state["eligibility_checks"][opportunity_id] = labels
    persist("eligibility_checks")


def set_donors(items: list[dict[str, Any]]) -> None:
    """Replace donor rows and persist when configured."""
    st.session_state[STATE_DONORS] = items
    repository = _repository()
    if repository:
        repository.save(STATE_DONORS, items)


def add_donor_if_missing(opportunity: dict[str, Any]) -> bool:
    """Add an opportunity donor once; return whether a row was added."""
    items = get_donors()
    if any(row.get("donor", "").casefold() == opportunity["donor"].casefold() for row in items):
        return False
    items.append(Donor(opportunity["donor"], opportunity=opportunity["id"], amount=opportunity["amount"], next_action="Verify source and eligibility").to_dict())
    set_donors(items)
    return True


def add_opportunity(item: Opportunity) -> None:
    """Add a uniquely identified opportunity."""
    items = get_opportunities()
    items.append(item.to_dict())
    set_opportunities(items)


def add_approval(item: ApprovalItem) -> None:
    """Append a draft to the human approval queue."""
    get_approvals().append(item.to_dict())
    persist(STATE_APPROVALS)


def save_org_profile() -> None:
    """Persist the editable profile model when configured."""
    persist(STATE_ORG)


def update_org_profile(values: dict[str, str]) -> None:
    """Update editable profile fields without marking them verified."""
    st.session_state[STATE_ORG].update(values)
    save_org_profile()


def save_org_fact_review(label: str, verified: bool) -> None:
    """Save a human-reviewed fact state."""
    st.session_state[STATE_ORG].setdefault("facts", {})[label] = verified
    save_org_profile()


def audit_user() -> str:
    """Return the demo reviewer label used by audit entries."""
    return st.session_state["audit_user"]


def org() -> OrgProfile:
    """Build the current profile model from state."""
    return OrgProfile(**st.session_state[STATE_ORG])


def export_state() -> dict[str, Any]:
    """Collect portable user-generated app data for JSON backup."""
    return {key: st.session_state[key] for key in (STATE_OPPORTUNITIES, STATE_DONORS, STATE_APPROVALS, STATE_ORG, "eligibility_checks", "documents", "followups", "proposal_versions")}


def import_state(data: dict[str, Any]) -> None:
    """Restore a JSON backup after checking required record collections."""
    if not isinstance(data, dict):
        raise ValueError("Backup root must be a JSON object.")
    collection_keys = (STATE_OPPORTUNITIES, STATE_DONORS, STATE_APPROVALS)
    if not all(isinstance(data.get(key), list) for key in collection_keys) or not isinstance(data.get(STATE_ORG), dict):
        raise ValueError("Backup is missing a required data section.")
    if not all(isinstance(row, dict) for key in collection_keys for row in data[key]):
        raise ValueError("Backup record collections must contain JSON objects.")
    required_rows = {
        STATE_OPPORTUNITIES: {"id", "donor", "title", "source", "status"},
        STATE_DONORS: {"id", "donor", "stage"},
        STATE_APPROVALS: {"id", "item", "item_type", "status", "created"},
    }
    for key, fields in required_rows.items():
        if any(not fields.issubset(row) for row in data[key]):
            raise ValueError(f"Backup contains an incomplete {key} record.")
    profile_fields = {"name", "focus", "registration", "tax_status", "csr1", "annual_budget", "beneficiaries", "facts"}
    if not profile_fields.issubset(data[STATE_ORG]):
        raise ValueError("Backup organisation profile is incomplete.")
    for key, value in data.items():
        if key in export_state():
            st.session_state[key] = value
            persist(key)
