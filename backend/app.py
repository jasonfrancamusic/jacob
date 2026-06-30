from __future__ import annotations

from fastapi import FastAPI

from api.schemas import ChatRequest, ChatResponse, HealthResponse, ReflectionResponse
from jacob_core import __version__
from jacob_core.core import JacobCore
from jacob_core.models import PartnerMessage

app = FastAPI(
    title="Jacob Core API",
    description="First API layer for Jacob 0.1 — Personal AI Partner.",
    version=__version__,
)

core = JacobCore()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="jacob-core-api", version=__version__)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    response = core.handle(
        PartnerMessage(
            partner_name=request.partner_name,
            content=request.message,
            metadata=request.metadata,
        )
    )

    suggested_memory = None
    if response.reflection.suggested_memory:
        suggested_memory = {
            "key": response.reflection.suggested_memory.key,
            "value": response.reflection.suggested_memory.value,
            "category": response.reflection.suggested_memory.category,
            "authorized": response.reflection.suggested_memory.authorized,
        }

    return ChatResponse(
        text=response.text,
        intent=response.intent.value,
        specialist_name=response.specialist_name,
        reflection=ReflectionResponse(
            helped=response.reflection.helped,
            should_follow_up=response.reflection.should_follow_up,
            suggested_memory=suggested_memory,
            notes=response.reflection.notes,
        ),
        debug=response.debug,
    )
