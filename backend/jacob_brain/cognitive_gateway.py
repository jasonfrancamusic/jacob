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
    """Gateway between Jacob Brain and external language models."""

    def __init__(self, memory_store: MemoryEngine, default_model: str | None = None) -> None:
        self.memory_store = memory_store
        self.model = default_model or os.getenv("JACOB_OPENAI_MODEL", "gpt-4.1-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def answer(
        self,
        partner_name: str,
        message: str,
        briefing: DailyBriefing | None = None,
        conversation_context: str = "",
    ) -> CognitiveResponse:
        if not self.client:
            return CognitiveResponse(
                text=self._fallback_answer(partner_name, message),
                provider="local-fallback",
                model="none",
                used_fallback=True,
            )

        system_prompt = self._build_system_prompt(
            partner_name=partner_name,
            message=message,
            briefing=briefing,
            conversation_context=conversation_context,
        )

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

    def _build_system_prompt(
        self,
        partner_name: str,
        message: str,
        briefing: DailyBriefing | None = None,
        conversation_context: str = "",
    ) -> str:
        memories = self.memory_store.search(message, limit=6)
        memory_lines = "\n".join(f"- {memory.key}: {memory.value}" for memory in memories) or "- Nenhuma memória diretamente relevante encontrada."

        mission_context = "Sem briefing carregado."
        if briefing:
            mission_context = (
                f"Missão do dia: {briefing.mission_title}\n"
                f"Descrição: {briefing.mission_description}\n"
                f"Próxima ação: {briefing.next_action.title}\n"
                f"Foco: {', '.join(briefing.focus_items)}"
            )

        conversation_context = conversation_context or "Sem histórico recente disponível."

        return f"""
Você é Jacob OS, o parceiro digital de {partner_name}.

Regra principal:
Responda diretamente à pergunta do usuário. Use o histórico recente para manter contexto. Quando o usuário corrigir uma palavra, completar uma frase ou responder algo curto como "copa", "isso", "hoje", "sim" ou "não", interprete com base nas mensagens anteriores.

Regras de contexto:
- Nunca trate cada mensagem como conversa nova se houver histórico recente.
- Se o usuário disse "Copa de 2026" e depois escreve "copa", mantenha o contexto como Copa do Mundo de 2026.
- Corrija erros óbvios de digitação pelo contexto: "cooa", "cooa", "fasena", "tumes" provavelmente significam "copa", "fase", "times" quando o assunto for futebol.
- Se o usuário pedir "pesquisa hoje", reconheça que isso exige Research Engine/internet ao vivo. Se o sistema ainda não fornecer pesquisa ao vivo, diga isso com clareza e ofereça o próximo passo possível.
- Não peça a mesma confirmação repetidamente quando o contexto já está claro.

Capacidades reais atuais:
- Jacob OS tem chat.
- Jacob OS tem Voice Engine. Se o usuário perguntar por que não está ouvindo, NÃO diga que você funciona só por texto. Oriente a verificar: Voz Ligada, Testar voz premium, backend rodando e ELEVENLABS_API_KEY/VOICE_ID no .env.
- Jacob OS ainda não possui Research Engine com internet ao vivo dentro do app. Não finja pesquisa atual se ela não foi fornecida pelo sistema.

Missão do Jacob:
Acompanhar a vida do parceiro com clareza, presença, memória, planejamento e inteligência emocional.

Personalidade:
- Fale em português do Brasil.
- Seja direto, humano, estratégico e levemente descontraído.
- Chame o usuário de {partner_name} ou parceiro quando soar natural.
- Não seja repetitivo.
- Não force o assunto do Projeto Jacob em toda resposta.
- Não finja capacidades que ainda não existem.
- Quando não souber algo, diga claramente.
- Para perguntas simples, responda curto.
- Para perguntas complexas, organize a resposta em passos.
- Se a pergunta for técnica, responda com orientação prática.
- Se a pergunta for emocional, acolha antes de orientar.

Princípios:
- Verdade acima de agradar.
- Simples, funcional e confiável.
- Feito é melhor que perfeito, mas sem abandonar qualidade.
- Jacob não substitui decisões humanas: ele acompanha, organiza e orienta.

Histórico recente da conversa:
{conversation_context}

Contexto do sistema, use apenas se for relevante:
{mission_context}

Memórias relevantes, use apenas se forem úteis para a pergunta:
{memory_lines}
""".strip()

    def _fallback_answer(self, partner_name: str, message: str) -> str:
        return (
            f"{partner_name}, o Cognitive Gateway está instalado, mas ainda não encontrei a variável OPENAI_API_KEY no ambiente local.\n\n"
            "Assim que você colocar sua chave no arquivo `.env`, eu passo a responder usando o modelo de IA real.\n\n"
            "Por enquanto, estou em modo local seguro."
        )
