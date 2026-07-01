from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass
class KnowledgeRecord:
    title: str
    summary: str
    topic: str = "general"
    source: str = "manual"
    confidence: float = 0.7
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "topic": self.topic,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
        }


class KnowledgeCore:
    """General knowledge store for Jacob.

    This is intentionally separated from private partner memory.
    It stores reusable public learning only.
    """

    def __init__(self, path: str = "data/general_knowledge.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_records(self, topic: str | None = None, limit: int = 100) -> list[KnowledgeRecord]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        records = [self._from_dict(item) for item in raw]
        if topic:
            records = [item for item in records if item.topic == topic]
        return records[-limit:]

    def add_record(self, record: KnowledgeRecord) -> KnowledgeRecord:
        records = self.list_records(limit=5000)
        records.append(record)
        self._save(records)
        return record

    def search(self, query: str, limit: int = 10) -> list[KnowledgeRecord]:
        query_lower = query.lower()
        results = []
        for record in self.list_records(limit=5000):
            haystack = f"{record.title} {record.summary} {record.topic}".lower()
            if query_lower in haystack or any(word in haystack for word in query_lower.split() if len(word) > 3):
                results.append(record)
        return results[-limit:]

    def _save(self, records: list[KnowledgeRecord]) -> None:
        self.path.write_text(json.dumps([item.as_dict() for item in records], ensure_ascii=False, indent=2), encoding="utf-8")

    def _from_dict(self, data: dict[str, Any]) -> KnowledgeRecord:
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return KnowledgeRecord(
            id=data.get("id", str(uuid4())),
            title=data["title"],
            summary=data["summary"],
            topic=data.get("topic", "general"),
            source=data.get("source", "manual"),
            confidence=float(data.get("confidence", 0.7)),
            created_at=created_at or datetime.utcnow(),
        )
