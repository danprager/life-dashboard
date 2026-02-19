## Why

The dashboard currently only runs locally. Deploying to Render via GitHub gives it a public URL and enables automatic deploys on every push to `main`, with no infrastructure management.

## What Changes

- Add `render.yaml` at the repo root defining a single Web Service: build installs frontend + backend deps, start command runs uvicorn
- Update `backend/main.py`: remove `CORSMiddleware`, add `StaticFiles` mount so FastAPI serves the built Vue frontend at `/`
- Update `frontend/src/services/api.js`: set `baseURL: ''` (relative paths) so API calls work on the same origin in production
- Add Vite dev proxy in `vite.config.js` so local dev still routes `/api` to `http://localhost:8000` without CORS

## Capabilities

### New Capabilities
- `render-deployment`: Single Render Web Service at `https://life-dashboard.onrender.com` serving both the API and the Vue frontend

### Modified Capabilities
<!-- None -->

## Impact

- **`render.yaml`** (new, repo root): single Python Web Service with combined build + start commands
- **`backend/main.py`**: remove CORSMiddleware; mount `frontend/dist` as StaticFiles at `/`
- **`frontend/src/services/api.js`**: `baseURL` changed from `VITE_API_BASE_URL || 'http://localhost:8000'` to `''`
- **`frontend/vite.config.js`**: add `server.proxy` for `/api` → `http://localhost:8000`
- No env vars required on Render
- No changes to application logic, models, or tests
