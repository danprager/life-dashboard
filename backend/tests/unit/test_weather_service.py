"""
Unit tests for weather service.
Tests the service logic in isolation — external HTTP calls are mocked.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch

from app.services.weather import get_weather


# TODO: implement tests as part of TDD workflow
# Example structure:

# @pytest.mark.asyncio
# async def test_get_weather_returns_response():
#     with patch("app.services.weather.httpx.AsyncClient") as mock_client:
#         ...
#         result = await get_weather("Sydney", "AU")
#         assert result.location == "Sydney, AU"
#         assert isinstance(result.temperature, float)
