"""
Integration tests for weather endpoints.
Tests the API layer using FastAPI's TestClient — real HTTP routing, mocked services.
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app
from app.models.weather import DayForecast, WeatherResponse

client = TestClient(app)

MOCK_DAY_FORECASTS = [
    DayForecast(day="F", temp_min=13, temp_max=23),
    DayForecast(day="S", temp_min=11, temp_max=21),
    DayForecast(day="S", temp_min=10, temp_max=20),
    DayForecast(day="M", temp_min=12, temp_max=22),
    DayForecast(day="T", temp_min=14, temp_max=24),
    DayForecast(day="W", temp_min=13, temp_max=25),
    DayForecast(day="T", temp_min=11, temp_max=23),
]


def make_weather(name: str, bom_base: str) -> WeatherResponse:
    return WeatherResponse(
        location=name,
        temperature=18.0,
        description="Partly cloudy",
        humidity=55,
        wind_speed=12.0,
        temp_min=11.0,
        temp_max=24.0,
        forecast_7day=MOCK_DAY_FORECASTS,
        bom_today_url=bom_base + "#today",
        bom_7day_url=bom_base + "#7-days",
    )


MOCK_RESPONSES = [
    make_weather("Castlemaine", "https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine"),
    make_weather("Melbourne", "https://www.bom.gov.au/location/australia/victoria/central/bvic_pt042-melbourne"),
    make_weather("Sorrento", "https://www.bom.gov.au/location/australia/victoria/central/o2607452563-sorrento"),
]


def test_weather_all_locations_returns_three():
    with patch("app.routers.weather.get_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = MOCK_RESPONSES
        response = client.get("/api/weather/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_weather_all_locations_names():
    with patch("app.routers.weather.get_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = MOCK_RESPONSES
        response = client.get("/api/weather/")
    names = [item["location"] for item in response.json()]
    assert "Castlemaine" in names
    assert "Melbourne" in names
    assert "Sorrento" in names


def test_weather_response_has_new_fields():
    with patch("app.routers.weather.get_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = MOCK_RESPONSES
        response = client.get("/api/weather/")
    item = response.json()[0]
    assert "temp_min" in item
    assert "temp_max" in item
    assert "forecast_7day" in item
    assert "bom_today_url" in item
    assert "bom_7day_url" in item


def test_weather_forecast_7day_has_seven_entries():
    with patch("app.routers.weather.get_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = MOCK_RESPONSES
        response = client.get("/api/weather/")
    forecast = response.json()[0]["forecast_7day"]
    assert len(forecast) == 7


def test_weather_bom_urls_have_correct_anchors():
    with patch("app.routers.weather.get_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = MOCK_RESPONSES
        response = client.get("/api/weather/")
    item = response.json()[0]
    assert item["bom_today_url"].endswith("#today")
    assert item["bom_7day_url"].endswith("#7-days")
