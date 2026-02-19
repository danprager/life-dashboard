## ADDED Requirements

### Requirement: Single Render Web Service definition
The repository SHALL contain a `render.yaml` at the repo root defining a single Web Service named `life-dashboard` with:
- `runtime: python`
- `pythonVersion: "3.11"`
- `buildCommand` that installs frontend Node dependencies, builds the Vue app, then installs Python dependencies
- `startCommand` that runs uvicorn from the `backend/` directory on `$PORT`

#### Scenario: render.yaml present at repo root
- **WHEN** the repository is cloned
- **THEN** `render.yaml` exists at the repo root and defines a service named `life-dashboard`

#### Scenario: Build command installs both frontend and backend dependencies
- **WHEN** the Render build runs
- **THEN** it executes `npm install && npm run build` in `frontend/` followed by `pip install -r requirements.txt` in `backend/`

#### Scenario: Start command runs from backend directory
- **WHEN** the service starts
- **THEN** uvicorn is invoked from `backend/` so that `config.yaml` and `main.py` resolve correctly

---

### Requirement: FastAPI serves built frontend as static files
`backend/main.py` SHALL mount the built Vue frontend at `/` using FastAPI's `StaticFiles` with `html=True`. The static mount SHALL be registered after all API routes so that `/api/...` routes take priority.

The path to `frontend/dist` SHALL be resolved relative to `main.py`'s location (using `Path(__file__).parent`) so it is independent of the working directory.

#### Scenario: Frontend loads from root URL
- **WHEN** a GET request is made to `https://life-dashboard.onrender.com/`
- **THEN** the Vue `index.html` is returned

#### Scenario: API routes take priority over static files
- **WHEN** a GET request is made to `/api/health`
- **THEN** the health endpoint responds with `{"status": "ok"}`, not a static file

#### Scenario: Vue Router deep links return index.html
- **WHEN** a GET request is made to an unknown path (e.g. `/some/deep/link`)
- **THEN** `index.html` is returned (enabling client-side routing)

---

### Requirement: CORSMiddleware removed from production backend
`CORSMiddleware` SHALL be removed from `backend/main.py`. CORS is not required because the frontend and backend are served from the same origin in production.

#### Scenario: No CORS headers in production
- **WHEN** the API receives a same-origin request in production
- **THEN** no `Access-Control-Allow-Origin` headers are required or set by middleware

---

### Requirement: Frontend uses relative API paths
`frontend/src/services/api.js` SHALL set `baseURL: ''` so all API requests use paths relative to the current origin (e.g. `/api/weather/`). This works in both production (same-origin FastAPI) and local dev (Vite proxy).

#### Scenario: API calls use relative paths
- **WHEN** the frontend calls `weatherApi.getAll()`
- **THEN** the request is made to `/api/weather/` with no hardcoded host

---

### Requirement: Vite dev server proxies API requests
`frontend/vite.config.js` SHALL configure a `server.proxy` entry that forwards all `/api` requests to `http://localhost:8000` during local development. This preserves the existing local dev workflow without requiring CORS.

#### Scenario: Local dev API calls are proxied
- **WHEN** the Vite dev server is running and the frontend calls `/api/weather/`
- **THEN** the request is forwarded to `http://localhost:8000/api/weather/`

#### Scenario: Production build is unaffected by proxy config
- **WHEN** `npm run build` is executed
- **THEN** the proxy configuration has no effect on the built static files
