"""Export and escaping helpers."""
import html
import json
from typing import Any


def escape_html(value: object) -> str:
    """Escape untrusted values before safe HTML interpolation."""
    return html.escape(str(value), quote=True)


def json_backup(state: dict[str, Any]) -> str:
    """Serialize session data into a portable JSON backup."""
    return json.dumps(state, ensure_ascii=False, indent=2, default=str)
