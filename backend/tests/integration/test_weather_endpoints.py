"""
Integration tests for weather endpoints.
Tests the API layer using FastAPI's TestClient — real HTTP routing, mocked services.
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# TODO: implement tests as part of TDD workflow
# Example structure:

# def test_health_check():
#     response = client.get("/api/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

# def test_weather_all_locations():
#     response = client.get("/api/weather/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
