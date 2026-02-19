## 1. Frontend — Local Dev Proxy

- [x] 1.1 Add `server.proxy` to `frontend/vite.config.js` to forward `/api` requests to `http://localhost:8000` during dev
- [x] 1.2 Update `frontend/src/services/api.js` to set `baseURL: ''`

## 2. Backend — Serve Static Files

- [x] 2.1 Remove `CORSMiddleware` from `backend/main.py`
- [x] 2.2 Add `StaticFiles` mount in `backend/main.py`: resolve `frontend/dist` relative to `Path(__file__).parent`, mount at `/` with `html=True` after all API routes

## 3. Render Configuration

- [x] 3.1 Add `render.yaml` at repo root defining the `life-dashboard` Web Service with `runtime: python`, `pythonVersion: "3.11"`, combined build command, and start command

## 4. Verify Locally

- [x] 4.1 Run `npm run build` in `frontend/` and confirm `dist/` is produced
- [x] 4.2 Start the backend with `uvicorn main:app --reload` from `backend/` and confirm `http://localhost:8000/` serves the built frontend
- [x] 4.3 Confirm `http://localhost:8000/api/health` returns `{"status": "ok"}`
- [x] 4.4 Confirm local dev still works: Vite dev server at `http://localhost:5174/` proxies API calls correctly

## 5. Deploy

- [x] 5.1 Commit and push to `main`
- [x] 5.2 On Render: connect the GitHub repo — Render detects `render.yaml` and creates the service automatically
- [x] 5.3 Verify `https://life-dashboard.onrender.com/api/health` returns `{"status": "ok"}`
- [x] 5.4 Verify `https://life-dashboard.onrender.com/` loads the dashboard with live weather data
