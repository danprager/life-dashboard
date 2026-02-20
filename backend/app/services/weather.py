from datetime import datetime

import httpx

from app.models.weather import DayForecast, WeatherResponse

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


async def get_weather(
    city: str,
    country: str,
    bom_url: str,
    fire_district: str = None,
    show_fire_danger: bool = False,
    fire_data: dict = None,
    latitude: float = None,
    longitude: float = None,
    location_name: str = None,
) -> WeatherResponse:
    async with httpx.AsyncClient() as client:
        # Step 1: resolve coordinates — use config values if provided, else geocode
        if latitude is not None and longitude is not None:
            lat, lon = latitude, longitude
            name = location_name or city
        else:
            geo = await client.get(GEOCODE_URL, params={"name": city, "count": 1, "country": country})
            geo.raise_for_status()
            results = geo.json().get("results", [])
            if not results:
                raise ValueError(f"Location not found: {city}, {country}")
            result = results[0]
            lat, lon = result["latitude"], result["longitude"]
            name = result["name"]

        # Step 2: fetch current weather + 8-day daily forecast in one call
        weather = await client.get(FORECAST_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "forecast_days": 8,
            "timezone": "auto",
        })
        weather.raise_for_status()
        data = weather.json()
        current = data["current"]
        daily = data["daily"]

    # Today min/max from daily index 0
    temp_min = daily["temperature_2m_min"][0]
    temp_max = daily["temperature_2m_max"][0]

    # 7-day forecast from daily indices 1–7
    forecast_7day = []
    for i in range(1, 8):
        date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        forecast_7day.append(DayForecast(
            day=date.strftime("%A")[0],
            temp_min=round(daily["temperature_2m_min"][i]),
            temp_max=round(daily["temperature_2m_max"][i]),
        ))

    # Attach fire data if available for this location's district
    total_fire_ban = False
    fire_danger = None
    if fire_district and fire_data:
        district_data = fire_data.get(fire_district, {})
        total_fire_ban = district_data.get("total_fire_ban", False)
        if show_fire_danger:
            fire_danger = district_data.get("fire_danger")

    code = current["weather_code"]
    return WeatherResponse(
        location=name,
        temperature=current["temperature_2m"],
        description=WMO_DESCRIPTIONS.get(code, "Unknown"),
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
        temp_min=temp_min,
        temp_max=temp_max,
        forecast_7day=forecast_7day,
        bom_today_url=bom_url + "#today",
        bom_7day_url=bom_url + "#7-days",
        total_fire_ban=total_fire_ban,
        fire_danger=fire_danger,
    )
