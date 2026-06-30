# Memory Engine 0.1

## Purpose

Memory Engine is the first persistent memory layer of Jacob OS.

Jacob should not merely answer messages. Jacob should build a useful, transparent and authorized memory with the partner.

## Principles

1. Consent — Jacob saves only authorized memories.
2. Transparency — the partner can list what Jacob remembers.
3. Control — the partner can delete memories.
4. Utility — Jacob should remember only what helps the partner.
5. Safety — destructive or sensitive actions require permission.

## Seven Memory Categories

1. Conversational — relevant conversation context.
2. Long Term — identity, preferences and stable facts.
3. Projects — Jacob, Digital Multiverso, Damas, PMRR and other active projects.
4. Habits — routines, schedules, patterns and consistency.
5. Emotional — meaningful emotional states and important life moments.
6. Spiritual — values, principles, faith and purpose.
7. Dreams — goals, visions, legacy and future plans.

## Current API

```text
GET    /memories
GET    /memories?category=projects
POST   /memories
DELETE /memories/{memory_id}
```

## Current Storage

Memory Engine 0.1 uses JSON storage:

```text
backend/data/memory.json
```

This is temporary. Future versions should use PostgreSQL and embeddings for semantic memory.

## Next Steps

- Add memory approval flow in the frontend.
- Add memory editing.
- Add semantic search.
- Add memory source tracking from conversations.
- Add partner-facing memory dashboard.
