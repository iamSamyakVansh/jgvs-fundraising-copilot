"""Budget arithmetic used by the proposal workflow."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetSummary:
    subtotal: float
    requested: float
    variance: float


def summarize_budget(items: dict[str, float], requested: float) -> BudgetSummary:
    """Return subtotal and request variance for non-negative line items."""
    if requested < 0 or any(value < 0 for value in items.values()):
        raise ValueError("Budget amounts must be non-negative.")
    subtotal = sum(items.values())
    return BudgetSummary(subtotal, requested, requested - subtotal)


def line_percentages(items: dict[str, float]) -> dict[str, float]:
    """Return each line item's share of the line-item subtotal."""
    total = sum(items.values())
    return {name: (value / total * 100 if total else 0.0) for name, value in items.items()}
