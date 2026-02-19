import httpx

from app.models.weather import WeatherResponse

# Open-Meteo — free, no API key required
# Docs: https://open-meteo.com/en/docs
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Rain showers", 82: "Violent rain showers",
    95: "Thunderstorm",
}


async def get_weather(city: str, country: str) -> WeatherResponse:
    async with httpx.AsyncClient() as client:
        # Step 1: geocode the city
        geo = await client.get(GEOCODE_URL, params={"name": city, "count": 1, "country": country})
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            raise ValueError(f"Location not found: {city}, {country}")

        result = results[0]
        lat, lon = result["latitude"], result["longitude"]

        # Step 2: fetch current weather
        weather = await client.get(FORECAST_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto",
        })
        weather.raise_for_status()
        current = weather.json()["current"]

    code = current["weather_code"]
    return WeatherResponse(
        location=f"{result['name']}, {country}",
        temperature=current["temperature_2m"],
        description=WMO_DESCRIPTIONS.get(code, "Unknown"),
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
    )
