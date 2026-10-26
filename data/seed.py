"""Clearly illustrative seed records. Replace only with source-verified data."""
from models import Donor, Opportunity, OrgProfile


def opportunities() -> list[Opportunity]:
    """Create illustrative opportunity examples with preserved source URLs."""
    return [
        Opportunity("Example Foundation A", "Rural Learning and Digital Inclusion Grant", "Education", "India", "₹10–25 lakh (illustrative)", "2026-12-15", "Indian nonprofit registration; audited financials; education outcomes", "https://example.org/grants/rural-learning", "Research complete", illustrative=True),
        Opportunity("Example CSR Programme B", "Community Livelihoods Initiative", "Livelihoods", "India", "₹15–40 lakh (illustrative)", "2027-01-20", "Eligible NGO; project plan; beneficiary and budget details", "https://example.org/csr/livelihoods", illustrative=True),
        Opportunity("Example Trust C", "Women-led Community Development", "Women empowerment", "North India", "₹5–15 lakh (illustrative)", "2026-11-30", "Women-focused outcomes; audited statements; registration evidence", "https://example.org/funding/women", illustrative=True),
    ]


def donors() -> list[Donor]:
    """Create synthetic donor pipeline examples matching the seed register."""
    return [
        Donor("Example Foundation A", opportunity="OP-001", stage="Research", amount="₹10–25 lakh", next_action="Verify eligibility"),
        Donor("Example CSR Programme B", opportunity="OP-002", stage="Qualified", amount="₹15–40 lakh", next_action="Request programme guidelines"),
        Donor("Example Trust C", opportunity="OP-003", stage="Drafting", amount="₹5–15 lakh", next_action="Collect verified organisation details"),
    ]


def org_profile() -> OrgProfile:
    """Return an intentionally incomplete organisation profile."""
    return OrgProfile()
