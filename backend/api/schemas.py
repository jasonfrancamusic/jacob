from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    partner_name: str = Field(default="Jason", description="Name of the partner talking to Jacob.")
    message: str = Field(..., min_length=1, description="Partner message to Jacob.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ReflectionResponse(BaseModel):
    helped: bool
    should_follow_up: bool
    suggested_memory: dict[str, Any] | None = None
    notes: str


class ChatResponse(BaseModel):
    text: str
    intent: str
    specialist_name: str
    reflection: ReflectionResponse
    debug: dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
