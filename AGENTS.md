# AGENTS.md — Jacob OS

## Product Mission

Jacob OS is a personal cognitive operating system. It is not only a chatbot. Every change must strengthen presence, memory, planning, clarity and execution.

## Development Roles

- Jason: founder, product owner and final decision maker.
- ChatGPT: product architect, UX strategist and technical reviewer.
- Codex: implementation engineer for code changes, tests and refactors.

## Core Principles

1. Preserve user control.
2. Never mix private memory with general knowledge.
3. Do not fake capabilities that are not implemented.
4. Prefer small stable modules over large fragile changes.
5. Keep the UI premium, calm, responsive and coherent.
6. Do not place floating elements over core interaction areas.
7. Every new capability must be testable.

## Repository Conventions

- `backend/`: FastAPI, engines and API contracts.
- `frontend/`: Jacob OS web interface.
- `docs/`: product, architecture, design and sprint documentation.
- `data/`: local runtime data, should not contain secrets.

## Coding Guidelines

- Keep modules small and named by capability.
- Avoid rewriting large files unless necessary.
- Add CSS layers for visual refinements when safer.
- Use clear commit messages.
- Keep `.env` private. Never commit real API keys.
- Update documentation when creating major engines or changing architecture.

## Testing Checklist

Before a task is considered done:

- Backend starts without import errors.
- Frontend loads without blocking the main screen.
- Chat still works.
- Voice controls do not overlap the chat.
- Layout remains usable on desktop and mobile.
- New modules degrade safely when API keys are missing.
