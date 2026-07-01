# Jacob OS v0.2 Architecture

## Product Direction

Jacob OS is no longer treated as a chatbot interface. It is a personal cognitive operating system.

The chat is one module. The product is the environment where Jacob lives.

## Core Modules

```text
Jacob OS
│
├── Presence Engine
├── Jacob Brain
├── Jacob Guardian
├── Memory Engine
├── Planner Engine
├── Timeline Engine
├── Cognitive Gateway
├── Life Map
├── Projects
├── Integrations
└── Chat
```

## Jacob Brain

Jacob Brain is responsible for direct reasoning and conversation.

Current capabilities:

- Daily briefing generation.
- Planner orchestration.
- Cognitive Gateway integration.
- Context preparation for language models.

## Jacob Guardian

Jacob Guardian is the silent observer layer.

It does not chat directly. It prepares context for Jacob Brain.

Current capabilities:

- Local observation of system state.
- Development status summary.
- Project and habit observations from Memory Engine.

Future capabilities:

- Gmail observations.
- Outlook observations.
- Calendar observations.
- GitHub activity monitoring.
- Figma design monitoring.
- Morning briefing preparation.

## Timeline Engine

Timeline Engine records important moments in the evolution of Jacob and, later, the user's life.

Current capabilities:

- Local JSON timeline.
- Bootstrap milestones.
- API endpoint for listing events.
- API endpoint for creating events.

## Sprint 005 Goal

The goal of Sprint 005 is not to add random features. It is to create the first foundation for presence and silent intelligence.

A good Jacob should not only answer.

A good Jacob should remember, observe, prepare and then speak.
