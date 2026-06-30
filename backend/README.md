# Backend

Backend services for Jacob 0.1.

## Current status

The first executable version of Jacob Core has been created in Python and exposed through a FastAPI API.

## Setup

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run CLI

```bash
python cli.py
```

Example prompts:

```text
Bom dia, Jacob.
Vamos planejar a Sprint 002 do Projeto Jacob.
Como está minha vida em métricas?
Estou cansado hoje.
```

## Run API

```bash
uvicorn app:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Chat endpoint:

```text
POST http://127.0.0.1:8000/chat
```

Example JSON:

```json
{
  "partner_name": "Jason",
  "message": "Bom dia, Jacob."
}
```

## Current modules

```text
backend/
  app.py
  cli.py
  requirements.txt
  api/
    __init__.py
    schemas.py
  jacob_core/
    __init__.py
    models.py
    memory.py
    specialists.py
    core.py
  tests/
    test_jacob_core.py
```

## What Jacob Core 0.1 already does

- Receives a partner message.
- Understands a simple intent.
- Infers a basic mental state.
- Consults a simple memory store.
- Routes to a specialist.
- Produces a response.
- Reflects after responding.
- Exposes `/health` and `/chat` through FastAPI.

## Next steps

- Add permission confirmation flow.
- Add API tests.
- Add real LLM provider integration.
- Add persistent database-backed memory.
- Connect frontend to the API.
