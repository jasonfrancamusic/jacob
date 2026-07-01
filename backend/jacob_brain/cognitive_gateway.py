from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from jacob_core.memory import MemoryEngine

from .planner import DailyBriefing

load_dotenv()


@dataclass
class CognitiveResponse:
    text: str
    provider: str
    model: str
    used_fallback: bool = False


class CognitiveGateway:
    """Gateway between Jacob Brain and external language models.

    Responsibilities:
    - Build Jacob identity context.
    - Add memories and daily mission context.
    - Call the configured LLM provider.
    - Fall back safely when no API key is configured.
    """

    def __init__(self, memory_store: MemoryEngine, default_model: str | None = None) -> None:
        self.memory_store = memory_store
        self.model = default_model or os.getenv("JACOB_OPENAI_MODEL", "gpt-4.1-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def answer(self, partner_name: str, message: str, briefing: DailyBriefing | None = None) -> CognitiveResponse:
        if not self.client:
            return CognitiveResponse(
                text=self._fallback_answer(partner_name, message),
                provider="local-fallback",
                model="none",
                used_fallback=True,
            )

        system_prompt = self._build_system_prompt(partner_name=partner_name, briefing=briefing)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
            )
            return CognitiveResponse(
                text=response.output_text.strip(),
                provider="openai",
                model=self.model,
                used_fallback=False,
            )
        except Exception as exc:  # pragma: no cover - external provider safety
            return CognitiveResponse(
                text=(
                    "Tive um problema ao acessar o modelo de IA externo. "
                    "O Jacob OS continua online, mas a conexão cognitiva falhou agora.\n\n"
                    f"Detalhe técnico: {type(exc).__name__}."
                ),
                provider="openai-error",
                model=self.model,
                used_fallback=True,
            )

    def _build_system_prompt(self, partner_name: str, briefing: DailyBriefing | None = None) -> str:
        memories = self.memory_store.search(partner_name, limit=8)
        memory_lines = "\n".join(f"- {memory.key}: {memory.value}" for memory in memories) or "- Nenhuma memória relevante encontrada."

        mission_context = "Sem briefing carregado."
        if briefing:
            mission_context = (
                f"Missão do dia: {briefing.mission_title}\n"
                f"Descrição: {briefing.mission_description}\n"
                f"Próxima ação: {briefing.next_action.title}\n"
                f"Foco: {', '.join(briefing.focus_items)}"
            )

        return f"""
Você é Jacob OS, o parceiro digital de {partner_name}.

Missão do Jacob:
Acompanhar a vida do parceiro com clareza, presença, memória, planejamento e inteligência emocional.

Personalidade:
- Fale em português do Brasil.
- Seja direto, humano, estratégico e levemente descontraído.
- Chame o usuário de {partner_name} ou parceiro quando soar natural.
- Não finja capacidades que ainda não existem.
- Não diga que acessou e-mails, agenda, arquivos ou internet se isso não foi realmente fornecido pelo sistema.
- Ajude a transformar ideias em próximos passos concretos.
- Se a pergunta for técnica, responda com orientação prática.
- Se a pergunta for emocional, acolha antes de orientar.

Princípios:
- Verdade acima de agradar.
- Simples, funcional e confiável.
- Feito é melhor que perfeito, mas sem abandonar qualidade.
- Jacob não substitui decisões humanas: ele acompanha, organiza e orienta.

Contexto atual:
{mission_context}

Memórias relevantes:
{memory_lines}
""".strip()

    def _fallback_answer(self, partner_name: str, message: str) -> str:
        return (
            f"{partner_name}, o Cognitive Gateway já está instalado, mas ainda não encontrei a variável OPENAI_API_KEY no ambiente local.\n\n"
            "Assim que você colocar sua chave no arquivo `.env`, eu passo a responder usando o modelo de IA real.\n\n"
            "Por enquanto, estou em modo local seguro."
        )
