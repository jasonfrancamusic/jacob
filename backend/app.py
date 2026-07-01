from __future__ import annotations

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MemoryCreateRequest,
    MemoryDeleteResponse,
    MemoryResponse,
    ReflectionResponse,
)
from jacob_brain import JacobBrain
from jacob_brain.cognitive_gateway import CognitiveGateway
from jacob_brain.conversation_history import ConversationHistory
from jacob_brain.timeline import TimelineEngine, TimelineEvent
from jacob_core import __version__
from jacob_core.core import JacobCore
from jacob_core.models import Intent, MemoryCategory, MemoryRecord
from jacob_guardian import JacobGuardian
from jacob_knowledge import KnowledgeCore, KnowledgeRecord
from jacob_research import ResearchEngine
from jacob_voice import VoiceEngine


class VoiceRequest(BaseModel):
    text: str


app = FastAPI(
    title="Jacob Core API",
    description="First API layer for Jacob 0.1 — Personal AI Partner.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

core = JacobCore()
brain = JacobBrain(core.memory_store)
cognitive_gateway = CognitiveGateway(core.memory_store)
guardian = JacobGuardian(core.memory_store)
timeline = TimelineEngine()
conversation_history = ConversationHistory()
knowledge_core = KnowledgeCore()
voice_engine = VoiceEngine()
research_engine = ResearchEngine()


def serialize_memory(memory: MemoryRecord) -> MemoryResponse:
    return MemoryResponse(
        id=memory.id,
        key=memory.key,
        value=memory.value,
        category=memory.category.value,
        authorized=memory.authorized,
        importance=memory.importance,
        source=memory.source,
        created_at=memory.created_at.isoformat(),
        updated_at=memory.updated_at.isoformat(),
    )


def recent_conversation_context(limit: int = 12) -> str:
    messages = conversation_history.list_messages(limit=limit)
    lines = []
    for message in messages:
        role = "Jason" if message.role == "user" else "Jacob"
        lines.append(f"{role}: {message.content}")
    return "\n".join(lines)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="jacob-core-api", version=__version__)


@app.get("/briefing")
def briefing(partner_name: str = "Jason") -> dict:
    payload = brain.daily_briefing(partner_name=partner_name).as_dict()
    payload["guardian"] = guardian.briefing_notes()
    return payload


@app.post("/voice/speak")
def speak(request: VoiceRequest) -> dict:
    return voice_engine.synthesize(request.text).as_dict()


@app.get("/research/search")
def research_search(q: str) -> dict:
    results = research_engine.search(q)
    return {"query": q, "results": [result.as_dict() for result in results]}


@app.get("/guardian")
def guardian_status() -> dict:
    return guardian.briefing_notes()


@app.get("/timeline")
def list_timeline() -> dict:
    return {"events": [event.as_dict() for event in timeline.list_events()]}


@app.post("/timeline")
def create_timeline_event(title: str, description: str, category: str = "development") -> dict:
    event = timeline.add_event(TimelineEvent(title=title, description=description, category=category))
    return event.as_dict()


@app.get("/conversations")
def list_conversation_messages(limit: int = 50) -> dict:
    return {"messages": [message.as_dict() for message in conversation_history.list_messages(limit=limit)]}


@app.delete("/conversations")
def clear_conversation_messages() -> dict:
    conversation_history.clear()
    return {"cleared": True}


@app.get("/knowledge")
def list_knowledge(topic: str | None = None, limit: int = 100) -> dict:
    return {"records": [record.as_dict() for record in knowledge_core.list_records(topic=topic, limit=limit)]}


@app.get("/knowledge/search")
def search_knowledge(q: str, limit: int = 10) -> dict:
    return {"records": [record.as_dict() for record in knowledge_core.search(q, limit=limit)]}


@app.post("/knowledge")
def create_knowledge(title: str, summary: str, topic: str = "general", source: str = "manual", confidence: float = 0.7) -> dict:
    record = knowledge_core.add_record(
        KnowledgeRecord(title=title, summary=summary, topic=topic, source=source, confidence=confidence)
    )
    return record.as_dict()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    context = recent_conversation_context(limit=12)
    conversation_history.add_message("user", request.message)

    research_context = ""
    research_results = []
    if research_engine.should_research(request.message):
        query = research_engine.normalize_query(request.message, context)
        research_results = research_engine.search(query)
        research_context = "\n\nPesquisa ao vivo disponível para esta pergunta:\n" + research_engine.format_results(research_results)

    daily_briefing = brain.daily_briefing(partner_name=request.partner_name)
    cognitive_response = cognitive_gateway.answer(
        partner_name=request.partner_name,
        message=request.message,
        briefing=daily_briefing,
        conversation_context=context + research_context,
    )

    conversation_history.add_message("assistant", cognitive_response.text)

    return ChatResponse(
        text=cognitive_response.text,
        intent=Intent.GENERAL_CONVERSATION.value,
        specialist_name="Cognitive Gateway",
        reflection=ReflectionResponse(
            helped=True,
            should_follow_up=True,
            suggested_memory=None,
            notes="Response generated through Cognitive Gateway with recent context and optional live research.",
        ),
        debug={
            "provider": cognitive_response.provider,
            "model": cognitive_response.model,
            "used_fallback": cognitive_response.used_fallback,
            "research_used": bool(research_results),
            "research_results": [result.as_dict() for result in research_results],
        },
    )


@app.get("/memories", response_model=list[MemoryResponse])
def list_memories(category: str | None = None) -> list[MemoryResponse]:
    parsed_category = MemoryCategory(category) if category else None
    return [serialize_memory(memory) for memory in core.memory_store.list_memories(parsed_category)]


@app.post("/memories", response_model=MemoryResponse)
def create_memory(request: MemoryCreateRequest) -> MemoryResponse:
    if not request.authorized:
        raise HTTPException(status_code=400, detail="Jacob cannot save unauthorized memory.")

    try:
        category = MemoryCategory(request.category)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid memory category.") from exc

    memory = MemoryRecord(
        key=request.key,
        value=request.value,
        category=category,
        authorized=request.authorized,
        importance=request.importance,
        source=request.source,
    )
    return serialize_memory(core.memory_store.add_memory(memory))


@app.delete("/memories/{memory_id}", response_model=MemoryDeleteResponse)
def delete_memory(memory_id: str) -> MemoryDeleteResponse:
    return MemoryDeleteResponse(deleted=core.memory_store.delete_memory(memory_id))
