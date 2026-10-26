"""Transparent eligibility readiness scoring; never an eligibility decision."""
from dataclasses import dataclass


CHECKS = [
    ("Registration and legal status verified", 20, "Donors commonly require current proof of legal registration."),
    ("Required 12A / 80G evidence verified", 15, "Tax status may be a donor requirement; check applicability and validity."),
    ("CSR-1 requirement checked", 10, "Some CSR funders require current CSR-1 evidence."),
    ("Geographic eligibility confirmed", 15, "The opportunity may be limited to specific regions."),
    ("Thematic fit confirmed with JGVS evidence", 15, "Use verified project documents to support thematic fit."),
    ("Audited financials and budget available", 15, "Funders often require audited accounts and a compliant budget."),
    ("Deadline and submission route verified", 10, "Confirm the live deadline and submission process at the source."),
]


@dataclass(frozen=True)
class EligibilityResult:
    score: int
    completed: int
    total: int
    readiness: str


def score_eligibility(checked: set[str]) -> EligibilityResult:
    """Calculate a weighted readiness score for human review."""
    score = sum(weight for label, weight, _ in CHECKS if label in checked)
    completed = sum(label in checked for label, _, _ in CHECKS)
    readiness = "Ready for human review" if score == 100 else "Partially ready" if score else "Not ready"
    return EligibilityResult(score, completed, len(CHECKS), readiness)
