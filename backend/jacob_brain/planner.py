from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from jacob_core.memory import MemoryEngine
from jacob_core.models import MemoryCategory, MemoryRecord


@dataclass
class PlanAction:
    title: str
    reason: str
    priority: str = "alta"


@dataclass
class DailyBriefing:
    partner_name: str
    greeting: str
    date_label: str
    mission_title: str
    mission_description: str
    mission_progress: int
    next_action: PlanAction
    focus_items: list[str] = field(default_factory=list)
    reminder: str = ""
    memory_context: list[dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "partner_name": self.partner_name,
            "greeting": self.greeting,
            "date_label": self.date_label,
            "mission_title": self.mission_title,
            "mission_description": self.mission_description,
            "mission_progress": self.mission_progress,
            "next_action": {
                "title": self.next_action.title,
                "reason": self.next_action.reason,
                "priority": self.next_action.priority,
            },
            "focus_items": self.focus_items,
            "reminder": self.reminder,
            "memory_context": self.memory_context,
        }


class PlannerEngine:
    """First planning engine for Jacob Brain 1.0.

    The engine is intentionally deterministic for now. Later it can combine
    memory, calendar, projects and LLM reasoning.
    """

    def __init__(self, memory_store: MemoryEngine) -> None:
        self.memory_store = memory_store

    def generate_daily_briefing(self, partner_name: str = "Jason") -> DailyBriefing:
        now = datetime.now()
        projects = self.memory_store.list_memories(MemoryCategory.PROJECTS)
        habits = self.memory_store.list_memories(MemoryCategory.HABITS)

        if projects:
            main_project = max(projects, key=lambda item: item.importance)
            mission_title = main_project.value
        else:
            mission_title = "Finalizar o Memory Engine"

        reminder = "Você rende melhor pela manhã. Aproveite este horário para trabalho profundo."
        if habits:
            reminder = habits[-1].value

        return DailyBriefing(
            partner_name=partner_name,
            greeting=f"Bom dia, {partner_name}.",
            date_label=now.strftime("%d/%m/%Y"),
            mission_title=mission_title,
            mission_description="Transformar o Jacob OS em um parceiro que lembra, planeja e acompanha sua evolução.",
            mission_progress=45,
            next_action=PlanAction(
                title="Conectar o Planner Engine ao painel",
                reason="Isso fará a Home deixar de ser fixa e começar a refletir o plano do dia.",
                priority="alta",
            ),
            focus_items=[
                "Finalizar Planner Engine",
                "Conectar briefing ao frontend",
                "Salvar decisões importantes na memória",
            ],
            reminder=reminder,
            memory_context=[
                {
                    "id": memory.id,
                    "key": memory.key,
                    "value": memory.value,
                    "category": memory.category.value,
                }
                for memory in projects[:3]
            ],
        )
