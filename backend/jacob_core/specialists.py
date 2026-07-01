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
            "• Prioridade estratégica: avançar no Jacob OS\n"
            "• Foco sugerido: uma entrega pequena, funcional e testável\n\n"
            "Minha sugestão para hoje: continuar simples, mas funcionando.\n\n"
            "Antes de começarmos: sua energia hoje está de 0 a 10?"
        )


class ProjectPlanningSpecialist(Specialist):
    name = "Project Planning Specialist"

    def respond(self, context: JacobContext) -> str:
        text = context.message.content.lower()
        if "próximo" in text or "proximo" in text or "passo" in text:
            return (
                "Próximo passo recomendado:\n\n"
                "1. Testar o painel atual.\n"
                "2. Confirmar que o chat responde pelo backend.\n"
                "3. Melhorar o Jacob Brain para gerar respostas mais úteis.\n"
                "4. Só depois conectar IA externa.\n\n"
                "Minha orientação: não pule para novas telas agora. Vamos fortalecer o cérebro."
            )

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
    name = "General Conversation Specialist"

    def respond(self, context: JacobContext) -> str:
        partner = context.message.partner_name
        message = context.message.content.strip()
        text = message.lower()

        if any(term in text for term in ["funcionando", "posso perguntar", "qualquer coisa", "teste"]):
            return (
                f"Sim, {partner}. Agora o chat está passando pelo backend e eu consigo responder pela lógica do Jacob Core.\n\n"
                "Ainda não estou conectado a um modelo de IA externo, então minhas respostas são do Jacob 0.1: "
                "simples, locais e baseadas em regras.\n\n"
                "Você já pode testar perguntas sobre:\n"
                "• o Projeto Jacob;\n"
                "• planejamento do dia;\n"
                "• mapa da vida;\n"
                "• próximos passos;\n"
                "• estado emocional.\n\n"
                "O próximo salto será conectar um modelo de IA para eu responder de forma realmente aberta."
            )

        if "quem é você" in text or "o que você é" in text:
            return (
                "Eu sou o Jacob OS 0.1: o primeiro protótipo do seu parceiro digital.\n\n"
                "Minha missão é transformar dados, memória e planejamento em direção prática para sua vida. "
                "Ainda estou nascendo, mas minha arquitetura já começou: Core, Brain, Planner, Memory e Presence."
            )

        if "obrigado" in text or "valeu" in text:
            return (
                "Tamo junto, parceiro.\n\n"
                "Cada teste que você faz me ajuda a ficar mais útil, mais claro e mais próximo da visão original do Jacob."
            )

        if "o que você lembra" in text or "memória" in text or "memoria" in text:
            memories = context.relevant_memories
            if not memories:
                return (
                    "Por enquanto eu tenho poucas memórias salvas.\n\n"
                    "O Memory Engine já existe, mas ainda estamos evoluindo a forma de registrar, aprovar, editar e usar memórias."
                )
            lines = ["Encontrei estas memórias relacionadas:\n"]
            for memory in memories[:5]:
                lines.append(f"• {memory.key}: {memory.value}")
            return "\n".join(lines)

        if "hora" in text or "horário" in text or "horario" in text:
            return (
                "Ainda não estou usando relógio contextual em tempo real dentro do Core.\n\n"
                "Mas essa função já está no nosso roadmap do Presence Engine: responder diferente de manhã, tarde, noite, fim de semana e rotina."
            )

        return (
            f"Entendi, {partner}.\n\n"
            f"Você disse: \"{message}\"\n\n"
            "Na versão atual, vou trabalhar assim:\n"
            "1. identificar o assunto;\n"
            "2. organizar em uma próxima ação;\n"
            "3. sugerir o caminho mais simples.\n\n"
            "Minha sugestão agora: transforme isso em uma pergunta prática ou peça um plano, e eu te respondo de forma mais objetiva."
        )


SPECIALISTS: dict[str, Specialist] = {
    "morning_briefing": MorningBriefingSpecialist(),
    "project_planning": ProjectPlanningSpecialist(),
    "life_analytics": LifeAnalyticsSpecialist(),
    "emotional_support": EmotionalSupportSpecialist(),
    "general_conversation": GeneralSpecialist(),
}
