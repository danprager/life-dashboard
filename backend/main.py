from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import weather

app = FastAPI(title="Life Dashboard API")

app.include_router(weather.router, prefix="/api/weather", tags=["weather"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# Serve built Vue frontend — must be mounted after all API routes
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
