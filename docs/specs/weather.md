# Spec: Weather Card

## Status
MVP — in progress

## Description
Display current weather conditions for one configured location.

## API
**Provider:** [Open-Meteo](https://open-meteo.com)
- Free, no API key required
- Uses geocoding API to resolve city name → lat/lon
- Uses forecast API to fetch current conditions

## Backend Endpoint
`GET /api/weather/` — returns weather for all configured locations
`GET /api/weather/{city}?country=AU` — returns weather for a single city

## Response Shape
```json
{
  "location": "Sydney, AU",
  "temperature": 22.4,
  "description": "Partly cloudy",
  "humidity": 65,
  "wind_speed": 15.2
}
```

## Frontend
- `WeatherCard.vue` — displays the weather data for one location
- Shown collapsed/expanded in the dashboard grid

## Configuration
Locations are defined in `backend/config.yaml`:
```yaml
locations:
  - name: Home
    city: Sydney
    country: AU
```

## Acceptance Criteria
- [ ] Backend returns current temperature, description, humidity, wind speed
- [ ] Frontend displays the card with all fields
- [ ] Card is collapsible
- [ ] Works for the first configured location
- [ ] Unit tests pass for service and endpoint layers

## Stretch
- Multiple locations (up to 3 initially)
- Configurable via UI
