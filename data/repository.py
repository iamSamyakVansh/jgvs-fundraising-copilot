"""Optional JSON-backed SQLite repository behind a small interface."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Protocol


class Repository(Protocol):
    """Persistence interface for optional local demo storage."""

    def load(self, key: str) -> dict | list | None: ...
    def save(self, key: str, value: dict | list) -> None: ...


class SQLiteRepository:
    """Store JSON records in a local SQLite key-value table."""

    def __init__(self, path: str | Path = "jgvs_demo.sqlite3") -> None:
        self.path = str(path)
        with sqlite3.connect(self.path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS records (key TEXT PRIMARY KEY, value TEXT NOT NULL)")

    def load(self, key: str) -> dict | list | None:
        """Load one JSON value, returning None when absent."""
        with sqlite3.connect(self.path) as connection:
            row = connection.execute("SELECT value FROM records WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def save(self, key: str, value: dict | list) -> None:
        """Save or replace one JSON value."""
        with sqlite3.connect(self.path) as connection:
            connection.execute("INSERT OR REPLACE INTO records VALUES (?, ?)", (key, json.dumps(value, ensure_ascii=False)))
