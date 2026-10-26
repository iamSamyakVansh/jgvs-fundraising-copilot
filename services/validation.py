"""Small validators shared by UI forms and unit tests."""
from datetime import date
from urllib.parse import urlparse
import re


def valid_url(value: str) -> bool:
    """Accept absolute HTTP(S) URLs with a hostname."""
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def valid_email(value: str) -> bool:
    """Validate an email address without attempting mailbox verification."""
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value.strip()))


def valid_date(value: str) -> bool:
    """Check an ISO-8601 calendar date."""
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def valid_number(value: object) -> bool:
    """Return whether a value can be interpreted as a non-negative number."""
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False
