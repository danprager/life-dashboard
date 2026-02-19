"""
Unit tests for weather service.
Tests the service logic in isolation — external HTTP calls are mocked.
"""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.weather import get_weather

BOM_URL = "https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine"

GEO_RESPONSE = {
    "results": [{"name": "Castlemaine", "latitude": -37.0688, "longitude": 144.2197}]
}

WEATHER_RESPONSE = {
    "current": {
        "temperature_2m": 17.8,
        "relative_humidity_2m": 55,
        "wind_speed_10m": 12.3,
        "weather_code": 2,
    },
    "daily": {
        "time": [
            "2026-02-19",
            "2026-02-20",
            "2026-02-21",
            "2026-02-22",
            "2026-02-23",
            "2026-02-24",
            "2026-02-25",
            "2026-02-26",
        ],
        "temperature_2m_max": [24.1, 23.4, 25.0, 21.3, 19.8, 22.5, 26.1, 24.7],
        "temperature_2m_min": [11.2, 12.7, 13.1, 10.5, 9.9, 11.8, 13.4, 12.0],
        "weather_code":       [2, 3, 61, 0, 1, 2, 3, 63],
    },
}


def make_mock_response(data: dict):
    mock = MagicMock()
    mock.raise_for_status = MagicMock()
    mock.json = MagicMock(return_value=data)
    return mock


@pytest.mark.asyncio
async def test_get_weather_returns_location():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    assert result.location == "Castlemaine"


@pytest.mark.asyncio
async def test_get_weather_current_conditions():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    assert result.temperature == 17.8
    assert result.description == "Partly cloudy"
    assert result.humidity == 55
    assert result.wind_speed == 12.3


@pytest.mark.asyncio
async def test_get_weather_today_min_max():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    assert result.temp_min == 11.2
    assert result.temp_max == 24.1


@pytest.mark.asyncio
async def test_get_weather_forecast_7day_length():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    assert len(result.forecast_7day) == 7


@pytest.mark.asyncio
async def test_get_weather_forecast_temperatures_are_integers():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    for day in result.forecast_7day:
        assert isinstance(day.temp_min, int)
        assert isinstance(day.temp_max, int)


@pytest.mark.asyncio
async def test_get_weather_forecast_first_day_is_tomorrow():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    # 2026-02-20 is a Friday
    assert result.forecast_7day[0].day == "F"
    assert result.forecast_7day[0].temp_min == 13   # round(12.7)
    assert result.forecast_7day[0].temp_max == 23   # round(23.4)


@pytest.mark.asyncio
async def test_get_weather_bom_urls():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=[
        make_mock_response(GEO_RESPONSE),
        make_mock_response(WEATHER_RESPONSE),
    ])
    with patch("app.services.weather.httpx.AsyncClient", return_value=mock_client):
        result = await get_weather("Castlemaine", "AU", BOM_URL)
    assert result.bom_today_url == BOM_URL + "#today"
    assert result.bom_7day_url == BOM_URL + "#7-days"
