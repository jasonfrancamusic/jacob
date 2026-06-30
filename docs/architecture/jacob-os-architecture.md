# Jacob OS — Architecture 0.1

## Architecture Principle

Jacob is not a single AI model.

Jacob is an orchestration layer that coordinates models, memory, agents, permissions and user interfaces.

## Main Modules

```text
User
  ↓
Jacob Interface
  ↓
Jacob Core
  ↓
┌───────────────┬───────────────┬───────────────┐
│ Jacob Memory  │ Jacob Agents  │ Jacob Connect │
└───────────────┴───────────────┴───────────────┘
  ↓
Model Layer: GPT | Gemini | Claude | Local Models
```

## Module 1 — Jacob Core

Responsible for:

- Understanding user intent.
- Choosing the correct agent.
- Preserving the Jacob personality.
- Routing tasks to integrations and models.

## Module 2 — Jacob Memory

Responsible for:

- Long-term partner memory.
- Goals.
- Preferences.
- Projects.
- Authorized facts.
- Personal context.

Jacob Memory is not a raw chat history. It is a structured knowledge layer about the partner.

## Module 3 — Jacob Connect

Responsible for connecting external services:

- Gmail.
- Outlook.
- Calendar.
- Drive.
- GitHub.
- Figma.
- Future integrations.

## Module 4 — Jacob Agents

Initial agents:

- Morning Briefing Agent.
- Daily Planner Agent.
- Email Assistant Agent.
- Calendar Assistant Agent.
- Founder Diary Agent.

## Module 5 — Jacob Personality

Responsible for keeping Jacob consistent even when the underlying AI model changes.

Jacob must sound like Jacob, not like the provider model.

## Module 6 — Jacob Voice

Future layer for:

- Voice input.
- Voice output.
- Wake word.
- Always-available presence.

## Security

Jacob must use permission levels:

1. Read.
2. Suggest.
3. Execute with confirmation.
4. Execute automatically after explicit saved permission.

No destructive action should be automatic in Jacob 0.1.