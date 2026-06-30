from __future__ import annotations

from .memory import SimpleMemoryStore
from .models import (
    EnergyLevel,
    Intent,
    JacobContext,
    JacobResponse,
    LifeMap,
    MemoryRecord,
    MentalState,
    PartnerMessage,
    Reflection,
)
from .specialists import SPECIALISTS


class JacobCore:
    """First executable nucleus of Jacob.

    Pipeline:
    1. Receive
    2. Understand intent
    3. Infer mental state
    4. Consult memory
    5. Route to specialist
    6. Respond
    7. Reflect
    """

    def __init__(self, memory_store: SimpleMemoryStore | None = None) -> None:
        self.memory_store = memory_store or SimpleMemoryStore()
        self.life_map = LifeMap()

    def handle(self, message: PartnerMessage) -> JacobResponse:
        intent = self._understand_intent(message.content)
        mental_state = self._infer_mental_state(message.content)
        relevant_memories = self.memory_store.search(message.content)
        specialist = SPECIALISTS.get(intent.value, SPECIALISTS[Intent.GENERAL_CONVERSATION.value])

        context = JacobContext(
            message=message,
            intent=intent,
            mental_state=mental_state,
            life_map=self.life_map,
            relevant_memories=relevant_memories,
            specialist_name=specialist.name,
        )

        response_text = specialist.respond(context)
        reflection = self._reflect(context, response_text)

        return JacobResponse(
            text=response_text,
            intent=intent,
            specialist_name=specialist.name,
            reflection=reflection,
            debug={
                "mental_state": mental_state.__dict__,
                "life_score": self.life_map.life_score(),
                "memories_used": len(relevant_memories),
            },
        )

    def _understand_intent(self, content: str) -> Intent:
        text = content.lower()
        if any(term in text for term in ["bom dia", "briefing", "acordei", "manhã"]):
            return Intent.MORNING_BRIEFING
        if any(term in text for term in ["sprint", "projeto", "planejar", "próximo passo", "github"]):
            return Intent.PROJECT_PLANNING
        if any(term in text for term in ["minha vida", "métricas", "mapa da vida", "dados", "dashboard"]):
            return Intent.LIFE_ANALYTICS
        if any(term in text for term in ["triste", "cansado", "ansioso", "desanimado", "preocupado"]):
            return Intent.EMOTIONAL_SUPPORT
        return Intent.GENERAL_CONVERSATION

    def _infer_mental_state(self, content: str) -> MentalState:
        text = content.lower()
        if any(term in text for term in ["cansado", "sono", "desanimado", "exausto"]):
            return MentalState(energy=EnergyLevel.LOW, mood="tired", confidence=0.7)
        if any(term in text for term in ["animado", "feliz", "empolgado", "vamos"]):
            return MentalState(energy=EnergyLevel.HIGH, mood="motivated", confidence=0.7)
        return MentalState()

    def _reflect(self, context: JacobContext, response_text: str) -> Reflection:
        suggested_memory = None
        if "jacob" in context.message.content.lower() and context.intent == Intent.PROJECT_PLANNING:
            suggested_memory = MemoryRecord(
                key="active_project",
                value="Jacob 0.1 is an active priority project for Jason França.",
                category="projects",
            )

        return Reflection(
            helped=True,
            should_follow_up=context.intent in {Intent.MORNING_BRIEFING, Intent.PROJECT_PLANNING},
            suggested_memory=suggested_memory,
            notes="Jacob should ask permission before saving suggested memory.",
        )
