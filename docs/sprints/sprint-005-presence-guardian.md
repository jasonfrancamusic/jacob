# Sprint 005 — Presence & Guardian

## Mission

Create the first foundation for Jacob OS v0.2: presence, silent observation and timeline memory.

## Deliverables

### 1. Jacob Guardian 0.1

Status: Implemented.

Guardian is a silent observer. It prepares observations for Jacob Brain.

Endpoint:

```text
GET /guardian
```

### 2. Timeline Engine 0.1

Status: Implemented.

Timeline stores important milestones in Jacob OS.

Endpoints:

```text
GET  /timeline
POST /timeline
```

### 3. Briefing + Guardian

Status: Implemented.

The `/briefing` endpoint now includes Guardian observations.

### 4. Presence Foundation

Status: Started.

The frontend already supports contextual greetings, local time and avatar switching.

Next:

- Opening ritual.
- Voice greeting.
- Presence state changes.

### 5. Memory Engine 2.0

Status: Planned.

Next:

- Memory dashboard.
- Edit memory.
- Approve suggested memory.
- Delete memory from interface.

## Strategic Rule

Do not make Jacob a chatbot with features.

Make Jacob OS a living environment where the partner enters and finds direction.
