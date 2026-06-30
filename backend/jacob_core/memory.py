from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import MemoryRecord


class SimpleMemoryStore:
    """Minimal JSON-based memory store for Jacob 0.1.

    This is intentionally simple. It will later be replaced by a proper
    database-backed memory layer.
    """

    def __init__(self, path: str = "data/memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_memories(self) -> list[MemoryRecord]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [self._from_dict(item) for item in raw]

    def search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        query_lower = query.lower()
        memories = self.list_memories()
        matches = [
            memory
            for memory in memories
            if query_lower in memory.key.lower()
            or query_lower in memory.value.lower()
            or query_lower in memory.category.lower()
        ]
        return matches[:limit]

    def add_memory(self, memory: MemoryRecord) -> None:
        memories = self.list_memories()
        memories.append(memory)
        payload = [self._to_dict(item) for item in memories]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _to_dict(self, memory: MemoryRecord) -> dict[str, str | bool]:
        return {
            "key": memory.key,
            "value": memory.value,
            "category": memory.category,
            "authorized": memory.authorized,
            "created_at": memory.created_at.isoformat(),
        }

    def _from_dict(self, data: dict) -> MemoryRecord:
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return MemoryRecord(
            key=data["key"],
            value=data["value"],
            category=data.get("category", "general"),
            authorized=data.get("authorized", True),
            created_at=created_at or datetime.utcnow(),
        )
