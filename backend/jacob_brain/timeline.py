from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass
class TimelineEvent:
    title: str
    description: str
    category: str = "development"
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
        }


class TimelineEngine:
    """Local timeline for Jacob OS milestones."""

    def __init__(self, path: str = "data/timeline.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")
            self._bootstrap()

    def list_events(self) -> list[TimelineEvent]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [self._from_dict(item) for item in raw]

    def add_event(self, event: TimelineEvent) -> TimelineEvent:
        events = self.list_events()
        events.append(event)
        self._save(events)
        return event

    def _save(self, events: list[TimelineEvent]) -> None:
        self.path.write_text(json.dumps([item.as_dict() for item in events], ensure_ascii=False, indent=2), encoding="utf-8")

    def _from_dict(self, data: dict[str, Any]) -> TimelineEvent:
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return TimelineEvent(
            id=data.get("id", str(uuid4())),
            title=data["title"],
            description=data["description"],
            category=data.get("category", "development"),
            created_at=created_at or datetime.utcnow(),
        )

    def _bootstrap(self) -> None:
        initial_events = [
            TimelineEvent("Jacob nasceu", "Primeira visão do parceiro digital foi definida."),
            TimelineEvent("Jacob Core API", "Backend inicial com FastAPI foi criado."),
            TimelineEvent("Jacob OS Command Center", "Primeira interface visual funcional foi implementada."),
            TimelineEvent("Memory Engine 0.1", "Jacob ganhou memória local autorizada."),
            TimelineEvent("Cognitive Gateway", "Jacob passou a poder usar um modelo de IA real."),
            TimelineEvent("Sprint 005", "Fundação do Guardian, Presence e Timeline foi iniciada."),
        ]
        self._save(initial_events)
