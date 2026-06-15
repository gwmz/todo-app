# TODO App

A personal TODO management web app with a beautiful, animated UI.

## Tech Stack

- **Frontend**: Vue 3 + Vite + TypeScript + TailwindCSS + Pinia
- **Backend**: Python FastAPI + SQLAlchemy + SQLite

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+

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

Open http://localhost:9000

### First-Time Setup

1. Start the backend
2. Open the frontend, click "Register" to create an account
3. Start adding tasks!
