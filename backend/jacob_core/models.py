from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Intent(str, Enum):
    """High-level intent understood by Jacob Core."""

    MORNING_BRIEFING = "morning_briefing"
    PROJECT_PLANNING = "project_planning"
    LIFE_ANALYTICS = "life_analytics"
    EMOTIONAL_SUPPORT = "emotional_support"
    GENERAL_CONVERSATION = "general_conversation"


class EnergyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class MentalState:
    """Operational mental state inferred or provided by the partner."""

    energy: EnergyLevel = EnergyLevel.MEDIUM
    mood: str = "neutral"
    focus_area: str | None = None
    confidence: float = 0.5


@dataclass
class PartnerMessage:
    """Input received from the partner."""

    partner_name: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LifeMap:
    """Seven-universe model for the partner's life."""

    health: int = 70
    family: int = 70
    spirituality: int = 70
    career: int = 70
    finances: int = 70
    knowledge: int = 70
    legacy: int = 70

    def as_dict(self) -> dict[str, int]:
        return {
            "health": self.health,
            "family": self.family,
            "spirituality": self.spirituality,
            "career": self.career,
            "finances": self.finances,
            "knowledge": self.knowledge,
            "legacy": self.legacy,
        }

    def life_score(self) -> int:
        values = list(self.as_dict().values())
        return round(sum(values) / len(values))


@dataclass
class MemoryRecord:
    """Simple authorized memory record."""

    key: str
    value: str
    category: str = "general"
    authorized: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class JacobContext:
    """Context used by Jacob Core while producing a response."""

    message: PartnerMessage
    intent: Intent
    mental_state: MentalState
    life_map: LifeMap
    relevant_memories: list[MemoryRecord] = field(default_factory=list)
    specialist_name: str = "General Specialist"


@dataclass
class Reflection:
    """Jacob's post-response reflection."""

    helped: bool
    should_follow_up: bool
    suggested_memory: MemoryRecord | None = None
    notes: str = ""


@dataclass
class JacobResponse:
    """Final response returned to the partner."""

    text: str
    intent: Intent
    specialist_name: str
    reflection: Reflection
    debug: dict[str, Any] = field(default_factory=dict)
