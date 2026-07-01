from __future__ import annotations

from jacob_core.memory import MemoryEngine
from jacob_core.models import MemoryCategory, MemoryRecord

from .planner import DailyBriefing, PlannerEngine


class JacobBrain:
    """Orchestration layer for Jacob OS.

    Jacob Brain is not the language model. It coordinates planning,
    memory and future presence behavior before the request reaches Jacob Core.
    """

    def __init__(self, memory_store: MemoryEngine) -> None:
        self.memory_store = memory_store
        self.planner = PlannerEngine(memory_store)
        self._bootstrap_default_memories()

    def daily_briefing(self, partner_name: str = "Jason") -> DailyBriefing:
        return self.planner.generate_daily_briefing(partner_name=partner_name)

    def _bootstrap_default_memories(self) -> None:
        existing = self.memory_store.search("jacob_current_project", limit=1)
        if existing:
            return

        self.memory_store.add_memory(
            MemoryRecord(
                key="jacob_current_project",
                value="Finalizar o Memory Engine e iniciar o Project Presence",
                category=MemoryCategory.PROJECTS,
                importance=5,
                source="system_bootstrap",
            )
        )
        self.memory_store.add_memory(
            MemoryRecord(
                key="jason_productivity_pattern",
                value="Você rende melhor pela manhã. Aproveite este horário para trabalho profundo.",
                category=MemoryCategory.HABITS,
                importance=4,
                source="system_bootstrap",
            )
        )
