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


class MemoryCreateRequest(BaseModel):
    key: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    category: str = Field(default="general")
    importance: int = Field(default=3, ge=1, le=5)
    authorized: bool = Field(default=True)
    source: str = Field(default="manual")


class MemoryResponse(BaseModel):
    id: str
    key: str
    value: str
    category: str
    authorized: bool
    importance: int
    source: str
    created_at: str
    updated_at: str


class MemoryDeleteResponse(BaseModel):
    deleted: bool
