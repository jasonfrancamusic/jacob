# Frontend

Frontend for Jacob 0.1.

## Current status

A simple mobile-first HTML/CSS/JS frontend is connected to the Jacob Core API.

## Files

```text
frontend/
  index.html
  styles.css
  app.js
```

## How to run

1. Start the backend API:

```bash
cd backend
uvicorn app:app --reload
```

2. Open the frontend:

You can open `frontend/index.html` directly in the browser.

Recommended local server option:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## Test prompts

```text
Bom dia, Jacob.
Como está minha vida em métricas?
Estou cansado hoje.
Vamos planejar a Sprint 002 do Projeto Jacob.
```

## Design direction

The interface follows the Cosmos Design System:

- Space-inspired.
- Calm futuristic presence.
- Glassmorphism.
- Digital Multiverso identity.
- Simple enough to work before becoming beautiful.
