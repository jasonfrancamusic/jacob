from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass
class ConversationMessage:
    role: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


class ConversationHistory:
    """Local persistent conversation history for Jacob OS."""

    def __init__(self, path: str = "data/conversation_history.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_messages(self, limit: int = 50) -> list[ConversationMessage]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        messages = [self._from_dict(item) for item in raw]
        return messages[-limit:]

    def add_message(self, role: str, content: str) -> ConversationMessage:
        message = ConversationMessage(role=role, content=content)
        messages = self.list_messages(limit=1000)
        messages.append(message)
        self._save(messages)
        return message

    def clear(self) -> None:
        self.path.write_text("[]", encoding="utf-8")

    def _save(self, messages: list[ConversationMessage]) -> None:
        self.path.write_text(json.dumps([item.as_dict() for item in messages], ensure_ascii=False, indent=2), encoding="utf-8")

    def _from_dict(self, data: dict[str, Any]) -> ConversationMessage:
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return ConversationMessage(
            id=data.get("id", str(uuid4())),
            role=data["role"],
            content=data["content"],
            created_at=created_at or datetime.utcnow(),
        )
