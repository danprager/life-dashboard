# Project Brief: Personal Life Dashboard

## Overview
A personal, self-hosted life dashboard displaying real-time data from public APIs.
Built as a learning project — each team member builds and runs their own instance,
with a stretch goal of sharing with family and friends.

---

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Backend        | Python, FastAPI, Uvicorn          |
| Frontend       | Vue 3, Vite, Axios                |
| Styling        | Vuetify (component library)       |
| Version Control| Git + GitHub                      |
| Deployment     | Local → Render (free tier)        |

---

## Architecture

- **Monorepo** — single repo with `/backend` and `/frontend` directories
- **Client-server** — Vue frontend calls FastAPI backend; backend calls external APIs
- **No database** — stateless; configuration via `.env` (secrets/API keys) and `config.yaml` (personal settings like locations)
- **Free-tier APIs only**

---

## MVP (Bare-bones)

- **Single card: Weather at one location**
- That's it — everything else is an extension

---

## Feature Roadmap (ad hoc, documented in `docs/specs/` as developed)

- Weather at 2nd and 3rd location
- Fire danger warnings
- Public transport
- Additional personal cards (team members add their own)

---

## UI

- Responsive grid of cards (desktop-first, mobile-friendly)
- Cards support collapse/expand for dense layouts
- Simple, clean Vuetify styling
- Adding a widget = adding a new card

---

## Ways of Working

- **Trunk-based development** — short-lived branches, frequent integration to `main`
- **Specs as code** — features and specs documented in `docs/specs/*.md`, evolving alongside the codebase
- **TDD** — aspire to write tests first
- **Verification** — automated tests in four layers:
  - Backend unit tests (`backend/tests/unit/`)
  - Endpoint/API integration tests (`backend/tests/integration/`)
  - Frontend unit tests (`frontend/src/tests/unit/`)
  - End-to-end tests (`frontend/src/tests/e2e/`)
- **Validation** — light manual testing

---

## Stretch Goals

- Configurable locations via UI (currently hardcoded in `config.yaml`)
- Shareable with family/friends via Render deployment
- Per-user widget personalisation
