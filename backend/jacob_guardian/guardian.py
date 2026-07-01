from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from jacob_core.memory import MemoryEngine
from jacob_core.models import MemoryCategory


@dataclass
class GuardianObservation:
    title: str
    description: str
    category: str = "system"
    priority: str = "normal"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }


class JacobGuardian:
    """Silent observation layer for Jacob OS 0.2.

    Guardian does not chat with the partner. It prepares context for Brain.
    Real integrations will be added later; this first version observes local state.
    """

    def __init__(self, memory_store: MemoryEngine) -> None:
        self.memory_store = memory_store

    def observe(self) -> list[GuardianObservation]:
        observations: list[GuardianObservation] = []
        project_memories = self.memory_store.list_memories(MemoryCategory.PROJECTS)
        habit_memories = self.memory_store.list_memories(MemoryCategory.HABITS)

        observations.append(
            GuardianObservation(
                title="Jacob OS está em modo desenvolvimento",
                description="O sistema já possui Frontend, Backend, Memory, Planner, Cognitive Gateway e início do Guardian.",
                category="development",
                priority="high",
            )
        )

        if project_memories:
            observations.append(
                GuardianObservation(
                    title="Projeto ativo detectado",
                    description=project_memories[-1].value,
                    category="project",
                    priority="high",
                )
            )

        if habit_memories:
            observations.append(
                GuardianObservation(
                    title="Padrão de produtividade disponível",
                    description=habit_memories[-1].value,
                    category="habit",
                    priority="normal",
                )
            )

        return observations

    def briefing_notes(self) -> dict[str, Any]:
        observations = self.observe()
        return {
            "status": "active",
            "summary": "Guardian ativo em modo local. Integrações externas serão conectadas nas próximas sprints.",
            "observations": [item.as_dict() for item in observations],
        }
