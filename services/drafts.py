"""Draft generation with explicit unknowns; never sends or submits content."""
from services.budget import summarize_budget


def concept_note(data: dict[str, object]) -> str:
    """Create a reviewable Markdown concept note from provided values."""
    items = data["items"]
    summary = summarize_budget(items, float(data["requested"]))
    lines = "\n".join(f"- {name}: ₹{value:,.0f}" for name, value in items.items())
    return f"""# Concept Note: {data['project']}

## Organisation
Jan Gramin Vikash Sansthan (JGVS)

## Project overview
**Geography:** {data['geography']}
**Duration:** {data['duration']} months
**Target beneficiaries:** {data['beneficiaries']}

## Objective
{data['objective']}

## Need and evidence
{data['evidence']}

## Proposed activities
{data['activities']}

## Expected outcomes
{data['outcomes']}

## Budget (INR)
{lines}

**Line-item subtotal:** ₹{summary.subtotal:,.0f}
**Requested budget:** ₹{summary.requested:,.0f}
**Variance:** ₹{summary.variance:,.0f}

## Information Required before submission
- Verified JGVS registration, 12A/80G and CSR-1 details where applicable
- Verified project location, beneficiary figures, needs evidence, and outcomes
- Donor-specific eligibility, format, deadline, and budget rules
- Approved organisation financials and authorised signatory
"""
