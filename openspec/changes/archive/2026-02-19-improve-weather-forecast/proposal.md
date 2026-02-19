## Why

The current weather feature shows a single configurable location with basic current conditions (temp, description, humidity, wind). We want to replace this with 3 fixed Victoria locations — Castlemaine, Melbourne, Sorrento — and enrich each card with today's min/max, a compact 7-day forecast, and direct links to official BOM forecasts.

## What Changes

- Replace the single Sydney location in `config.yaml` with 3 hardcoded Victorian locations: Castlemaine, Melbourne, Sorrento
- Extend the weather API response to include today's min/max and a 7-day daily forecast (starting tomorrow)
- Update the backend service to request daily forecast data from Open-Meteo alongside current conditions
- Redesign the `WeatherCard` component to display:
  - Current temperature (°C, prominent)
  - Today's min / max
  - Verbal description (e.g. "Partly cloudy")
  - Compact 7-day forecast: single-letter day abbreviation (M T W T F S S), min/max per day
  - Two static BOM links per location (today and 7-day), using the official BOM location pages with `#today` / `#7-days` anchors:
    - Castlemaine: `https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine#today` / `#7-days`
    - Melbourne: `https://www.bom.gov.au/location/australia/victoria/central/bvic_pt042-melbourne#today` / `#7-days`
    - Sorrento: `https://www.bom.gov.au/location/australia/victoria/central/o2607452563-sorrento#today` / `#7-days`
- Retain humidity and wind speed on the card
- **BREAKING**: `WeatherResponse` model gains new required fields (`temp_min`, `temp_max`, `forecast_7day`, `bom_today_url`, `bom_7day_url`)

## Capabilities

### New Capabilities
- `weather-forecast`: Full weather forecast feature — 3 default Victorian locations, enriched current + 7-day data from Open-Meteo, enhanced card UI with BOM links

### Modified Capabilities
<!-- None — no existing specs in openspec/specs/ -->

## Impact

- **Backend**
  - `backend/config.yaml`: Replace Sydney entry with Castlemaine, Melbourne, Sorrento (each with static BOM URLs)
  - `backend/app/models/weather.py`: Add `temp_min`, `temp_max`, `forecast_7day` (list of day objects), `bom_today_url`, `bom_7day_url`; retain `humidity`, `wind_speed`
  - `backend/app/services/weather.py`: Extend Open-Meteo request to include `daily` params (`temperature_2m_max`, `temperature_2m_min`, `weather_code`) for 8 days; build 7-day slice (indices 1–7); read BOM URLs from config
  - `backend/app/routers/weather.py`: Pass BOM URLs from config through to the service/response
- **Frontend**
  - `frontend/src/components/WeatherCard.vue`: New layout — current temp, today min/max, description, compact 7-day row, BOM links
  - No changes needed to `Dashboard.vue` or `api.js`
- **Tests**: Unit and integration tests for weather service and endpoint will need updating to match new model
