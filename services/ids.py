"""Stable identifiers for user-created records."""
from uuid import uuid4


def new_id() -> str:
    """Return a collision-resistant, readable record identifier."""
    return uuid4().hex
