from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import weather

app = FastAPI(title="Life Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/api/weather", tags=["weather"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
