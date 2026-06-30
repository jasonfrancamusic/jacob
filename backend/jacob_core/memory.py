from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import MemoryCategory, MemoryRecord


class MemoryEngine:
    """JSON-based Memory Engine for Jacob 0.1.

    Principles:
    - Consent: memory is saved only when authorized.
    - Transparency: memory can be listed and inspected.
    - Control: memory can be deleted by id.
    - Utility: memory is categorized for future reasoning.
    """

    def __init__(self, path: str = "data/memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_memories(self, category: MemoryCategory | None = None) -> list[MemoryRecord]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        memories = [self._from_dict(item) for item in raw]
        if category:
            return [memory for memory in memories if memory.category == category]
        return memories

    def search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        query_lower = query.lower().strip()
        if not query_lower:
            return self.list_memories()[:limit]

        memories = self.list_memories()
        matches = [
            memory
            for memory in memories
            if query_lower in memory.key.lower()
            or query_lower in memory.value.lower()
            or query_lower in memory.category.value.lower()
        ]
        return sorted(matches, key=lambda item: item.importance, reverse=True)[:limit]

    def add_memory(self, memory: MemoryRecord) -> MemoryRecord:
        if not memory.authorized:
            raise ValueError("Jacob cannot save unauthorized memory.")

        memories = self.list_memories()
        memories.append(memory)
        self._save(memories)
        return memory

    def delete_memory(self, memory_id: str) -> bool:
        memories = self.list_memories()
        remaining = [memory for memory in memories if memory.id != memory_id]
        if len(remaining) == len(memories):
            return False
        self._save(remaining)
        return True

    def clear(self) -> None:
        self.path.write_text("[]", encoding="utf-8")

    def _save(self, memories: list[MemoryRecord]) -> None:
        payload = [self._to_dict(item) for item in memories]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _to_dict(self, memory: MemoryRecord) -> dict:
        return {
            "id": memory.id,
            "key": memory.key,
            "value": memory.value,
            "category": memory.category.value,
            "authorized": memory.authorized,
            "importance": memory.importance,
            "source": memory.source,
            "created_at": memory.created_at.isoformat(),
            "updated_at": memory.updated_at.isoformat(),
        }

    def _from_dict(self, data: dict) -> MemoryRecord:
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        return MemoryRecord(
            id=data.get("id") or data.get("key", "memory"),
            key=data["key"],
            value=data["value"],
            category=MemoryCategory(data.get("category", MemoryCategory.GENERAL.value)),
            authorized=data.get("authorized", True),
            importance=int(data.get("importance", 3)),
            source=data.get("source", "manual"),
            created_at=created_at or datetime.utcnow(),
            updated_at=updated_at or datetime.utcnow(),
        )


# Backwards-compatible name used by JacobCore 0.1.
SimpleMemoryStore = MemoryEngine
