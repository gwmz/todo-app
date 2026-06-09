# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A personal TODO management web app with a Vue 3 frontend and FastAPI backend. SQLite for persistence, JWT for auth. The frontend proxies API calls to the backend via Vite's dev proxy.

## Architecture

```
todo-app/
├── backend/               # FastAPI + SQLAlchemy + SQLite
│   ├── app/
│   │   ├── main.py        # App entry, CORS, router includes
│   │   ├── database.py    # SQLite engine, session, Base
│   │   ├── models.py      # SQLAlchemy ORM (User, Category, Task)
│   │   ├── schemas.py     # Pydantic v2 request/response models
│   │   ├── crud.py        # DB operations for all resources
│   │   ├── core/config.py # Settings (SECRET_KEY, JWT config)
│   │   ├── core/security.py # Password hashing + JWT creation
│   │   └── api/
│   │       ├── auth.py       # /api/auth (register, login, me)
│   │       ├── categories.py # /api/categories (CRUD)
│   │       └── tasks.py      # /api/tasks (CRUD + search/filter)
│   └── requirements.txt
├── frontend/              # Vue 3 + Vite + TypeScript + TailwindCSS
│   ├── src/
│   │   ├── main.ts         # App bootstrap (Pinia + Router)
│   │   ├── App.vue         # Root component
│   │   ├── style.css       # Tailwind + glass-card/btn-primary/input-field utilities
│   │   ├── router.ts       # Vue Router with auth guards
│   │   ├── types/index.ts  # TypeScript interfaces (User, Task, Category, etc.)
│   │   ├── api/client.ts   # Axios instance with Bearer token interceptor
│   │   ├── stores/
│   │   │   ├── auth.ts     # Auth state (login, register, logout)
│   │   │   └── tasks.ts    # Task + category state + CRUD
│   │   ├── views/
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── MainLayout.vue  # Task list, add form, filters
│   │   │   └── SettingsView.vue # Category management
│   │   └── components/
│   │       ├── AddTaskForm.vue
│   │       └── TaskCard.vue
│   ├── vite.config.ts      # Proxy /api → backend
│   ├── tailwind.config.ts  # Custom animations, glass-card utility
│   └── package.json
└── docs/superpowers/       # Design specs and implementation plans
```

## Key Details

- **Auth flow**: JWT via `python-jose`. Backend uses bcrypt for password hashing. The `sub` claim in JWT is the user UUID. All protected endpoints use `get_current_user_id` dependency (OAuth2PasswordBearer) to extract the user from the Authorization header.
- **UUID handling**: SQLAlchemy UUID fields are typed as `str` in models but return Python `UUID` objects. All Pydantic response schemas have `field_validator` converters (`_to_str`) to serialize UUIDs to strings. Path parameters and JWT payloads also go through UUID conversion.
- **Port config**: Backend CORS and frontend Vite proxy must stay in sync. Default ports: backend `8080`, frontend `5180`.

## Commands

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

API docs: http://127.0.0.1:8080/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Web app: http://localhost:5180

Type check:
```bash
npx vue-tsc --noEmit
```

Build:
```bash
npm run build
```

### Full Stack

1. Start backend: `cd backend && uvicorn app.main:app --port 8080`
2. Start frontend: `cd frontend && npm run dev`
3. Open http://localhost:5180

## Development Notes

- No Docker, no test framework — direct local development with pip/npm.
- The SQLite database file is `backend/todo.db`. Delete it to reset.
- The README (`README.md`) references old default ports (8000/5173) — the actual running config uses 8080/5180. Update the README when ports change.
- Port conflicts are common on this machine (many dev tools use 8000-8100). If the default port is in use, pick another.
