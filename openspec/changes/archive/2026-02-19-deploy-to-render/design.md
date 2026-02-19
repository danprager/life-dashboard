## Context

The app is a monorepo with a FastAPI backend (`backend/`) and a Vue 3 + Vite frontend (`frontend/`). The goal is a single Render Web Service at `https://life-dashboard.onrender.com` where FastAPI serves both the API and the built frontend static files.

This is simpler than a two-service setup: one URL, no CORS configuration needed in production, no cross-service env var wiring.

## Goals / Non-Goals

**Goals:**
- Single Render Web Service serving both API and frontend from `https://life-dashboard.onrender.com`
- Auto-deploy on every push to `main`
- Local dev unchanged — frontend dev server and backend run separately as today

**Non-Goals:**
- Custom domain
- Separate staging environment
- CDN or caching optimisation

## Decisions

### 1. FastAPI serves the built frontend via `StaticFiles`

After all API routes are registered, `main.py` mounts the built frontend at `/`:

```python
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
```

`html=True` makes Render serve `index.html` for unknown paths, which is required for Vue Router's history mode. API routes registered before the mount take priority over the static handler.

The path `../frontend/dist` is resolved relative to `main.py` using `Path(__file__).parent` so it works regardless of which directory uvicorn is invoked from.

### 2. Vite dev proxy replaces the `VITE_API_BASE_URL` env var

In production, frontend and backend share the same origin so `axios` uses relative paths (`baseURL: ''`). In local dev, the Vite dev server proxies `/api` requests to `http://localhost:8000`, so the browser never makes a cross-origin request.

This means:
- No `VITE_API_BASE_URL` env var needed anywhere
- No CORS configuration needed — `CORSMiddleware` is removed from `main.py`
- `api.js` sets `baseURL: ''` (always relative)
- `vite.config.js` gains a `server.proxy` entry for `/api`

### 3. Single Render Web Service, no `rootDir`

The build command runs from the repo root, handling both frontend and backend in sequence. Render's Python runtime build image includes Node.js, so `npm` is available in the build step.

- **Build command:** `cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt`
- **Start command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

The `cd backend &&` prefix in the start command ensures `open("config.yaml")` resolves correctly (it uses a relative path).

### 4. Python version set via `render.yaml`

Pin `pythonVersion: "3.11"` to ensure reproducible builds regardless of Render's changing defaults.

## Risks / Trade-offs

- **`frontend/dist` missing if build fails** → FastAPI will start but `/` will 404. Mitigation: check build logs; the static mount is guarded with a path existence check so the API remains functional.
- **Free tier cold starts** → ~30s delay after ~15 min idle. Accepted.
- **Node in build image** → Render's standard build image includes Node; if this ever changes, the build command will fail clearly with a missing `npm` error.
- **`config.yaml` committed** → Contains only location names and public BOM URLs. No secrets.

## Migration Plan

1. Add Vite proxy to `vite.config.js`
2. Update `api.js` baseURL to `''`
3. Update `main.py`: remove CORSMiddleware, add StaticFiles mount
4. Add `render.yaml` to repo root
5. Push to `main`
6. On Render: connect GitHub repo → Render detects `render.yaml` → service created automatically
7. Verify: `https://life-dashboard.onrender.com/api/health` returns `{"status": "ok"}`
8. Verify: `https://life-dashboard.onrender.com/` loads the dashboard
