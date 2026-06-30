from __future__ import annotations

import json
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
        return [MemoryRecord(**item) for item in raw]

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
        payload = [memory.__dict__ | {"created_at": memory.created_at.isoformat()} for memory in memories]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
