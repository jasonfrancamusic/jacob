from __future__ import annotations

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
from jacob_core import __version__
from jacob_core.core import JacobCore
from jacob_core.models import Intent, MemoryCategory, MemoryRecord, PartnerMessage, Reflection

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


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="jacob-core-api", version=__version__)


@app.get("/briefing")
def briefing(partner_name: str = "Jason") -> dict:
    return brain.daily_briefing(partner_name=partner_name).as_dict()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    daily_briefing = brain.daily_briefing(partner_name=request.partner_name)
    cognitive_response = cognitive_gateway.answer(
        partner_name=request.partner_name,
        message=request.message,
        briefing=daily_briefing,
    )

    return ChatResponse(
        text=cognitive_response.text,
        intent=Intent.GENERAL_CONVERSATION.value,
        specialist_name="Cognitive Gateway",
        reflection=ReflectionResponse(
            helped=True,
            should_follow_up=True,
            suggested_memory=None,
            notes="Response generated through Cognitive Gateway.",
        ),
        debug={
            "provider": cognitive_response.provider,
            "model": cognitive_response.model,
            "used_fallback": cognitive_response.used_fallback,
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
