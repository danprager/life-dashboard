# Life Dashboard

A personal, self-hosted life dashboard. See [BRIEF.md](./BRIEF.md) for full project brief.

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add your API keys
uvicorn main:app --reload
```

Backend runs at http://localhost:8000
API docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test:unit
npm run test:e2e
```

## Project Structure

```
life-dashboard/
├── backend/           # FastAPI + Uvicorn
│   ├── app/
│   │   ├── models/    # Pydantic response models
│   │   ├── routers/   # API route handlers
│   │   └── services/  # External API clients
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── config.yaml    # Personal settings (locations etc.)
│   ├── .env.example   # API key template
│   └── main.py        # App entry point
├── frontend/          # Vue 3 + Vite
│   └── src/
│       ├── components/ # Reusable cards/widgets
│       ├── services/   # Axios API client
│       └── views/      # Page-level components
├── docs/
│   └── specs/         # Feature specs (.md)
└── BRIEF.md
```

## Configuration

Copy `backend/.env.example` to `backend/.env` and fill in your API keys.
Edit `backend/config.yaml` to set your location(s).
