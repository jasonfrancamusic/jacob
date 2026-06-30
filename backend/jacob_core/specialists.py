from __future__ import annotations

from abc import ABC, abstractmethod

from .models import JacobContext


class Specialist(ABC):
    """Base class for Jacob specialists."""

    name: str = "Base Specialist"

    @abstractmethod
    def respond(self, context: JacobContext) -> str:
        raise NotImplementedError


class MorningBriefingSpecialist(Specialist):
    name = "Morning Briefing Specialist"

    def respond(self, context: JacobContext) -> str:
        partner = context.message.partner_name
        life_score = context.life_map.life_score()

        return (
            f"Bom dia, {partner}. ☀️\n\n"
            "Vamos levantar, parceiro?\n\n"
            "Enquanto você começa o dia, organizei nosso primeiro briefing simples:\n\n"
            f"• Estado geral da vida: {life_score}%\n"
            "• Prioridade estratégica: avançar no Jacob 0.1\n"
            "• Foco sugerido: uma entrega pequena, funcional e testável\n\n"
            "Minha sugestão para hoje: continuar simples, mas funcionando.\n\n"
            "Antes de começarmos: sua energia hoje está de 0 a 10?"
        )


class ProjectPlanningSpecialist(Specialist):
    name = "Project Planning Specialist"

    def respond(self, context: JacobContext) -> str:
        return (
            "Vamos organizar isso como uma sprint.\n\n"
            "1. Definir a menor entrega útil.\n"
            "2. Criar algo executável.\n"
            "3. Testar.\n"
            "4. Melhorar.\n\n"
            "Para o Jacob, a regra continua: simples, funcional e confiável."
        )


class LifeAnalyticsSpecialist(Specialist):
    name = "Life Analytics Specialist"

    def respond(self, context: JacobContext) -> str:
        scores = context.life_map.as_dict()
        lines = ["Mapa da Vida — visão inicial:\n"]
        for area, score in scores.items():
            bars = "█" * round(score / 10) + "░" * (10 - round(score / 10))
            lines.append(f"• {area.title():<14} {bars} {score}%")
        lines.append("\nNão vou usar esses números para julgar você. Vou usá-los para encontrar direção.")
        return "\n".join(lines)


class EmotionalSupportSpecialist(Specialist):
    name = "Emotional Support Specialist"

    def respond(self, context: JacobContext) -> str:
        return (
            "Estou com você, parceiro.\n\n"
            "Nem todo momento precisa virar produtividade. Às vezes, o primeiro passo é respirar, "
            "organizar a mente e escolher apenas uma próxima ação.\n\n"
            "Quer que eu te ajude a reduzir o dia para uma única prioridade?"
        )


class GeneralSpecialist(Specialist):
    name = "General Specialist"

    def respond(self, context: JacobContext) -> str:
        return (
            "Entendi. Vou te ajudar com clareza e objetividade.\n\n"
            "Ainda estou na minha primeira versão, então vou começar pelo essencial: entender, organizar e sugerir o próximo passo."
        )


SPECIALISTS: dict[str, Specialist] = {
    "morning_briefing": MorningBriefingSpecialist(),
    "project_planning": ProjectPlanningSpecialist(),
    "life_analytics": LifeAnalyticsSpecialist(),
    "emotional_support": EmotionalSupportSpecialist(),
    "general_conversation": GeneralSpecialist(),
}
