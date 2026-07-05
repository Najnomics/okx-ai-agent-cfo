import json
import sqlite3
from pathlib import Path
from typing import Any


class LedgerStore:
    def __init__(self, data_dir: str) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "agent_cfo.sqlite3"
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def insert(self, record_id: str, kind: str, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO records (id, kind, payload_json) VALUES (?, ?, ?)",
                (record_id, kind, json.dumps(payload, sort_keys=True)),
            )

    def list_recent(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT payload_json, created_at FROM records ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        items = []
        for row in rows:
            item = json.loads(row["payload_json"])
            item["created_at"] = row["created_at"]
            items.append(item)
        return items

