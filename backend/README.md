# Backend

Backend services for Jacob 0.1.

## Current status

The first executable version of Jacob Core has been created in Python.

## How to run locally

From the repository root:

```bash
cd backend
python cli.py
```

Example prompts:

```text
Bom dia, Jacob.
Vamos planejar a Sprint 002 do Projeto Jacob.
Como está minha vida em métricas?
Estou cansado hoje.
```

## Current modules

```text
backend/
  cli.py
  requirements.txt
  jacob_core/
    __init__.py
    models.py
    memory.py
    specialists.py
    core.py
```

## What Jacob Core 0.1 already does

- Receives a partner message.
- Understands a simple intent.
- Infers a basic mental state.
- Consults a simple memory store.
- Routes to a specialist.
- Produces a response.
- Reflects after responding.

## Next steps

- Fix and improve persistent memory.
- Add permission confirmation flow.
- Add tests.
- Add FastAPI endpoint.
- Connect to a real LLM provider.
