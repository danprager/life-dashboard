## 1. Config

- [x] 1.1 Replace the Sydney entry in `backend/config.yaml` with three entries for Castlemaine, Melbourne, and Sorrento, each with `city`, `country`, and `bom_url` fields

## 2. Backend — Data Model

- [x] 2.1 Add `DayForecast` sub-model to `backend/app/models/weather.py` with fields: `day: str`, `temp_min: int`, `temp_max: int`
- [x] 2.2 Extend `WeatherResponse` with `temp_min: float`, `temp_max: float`, `forecast_7day: list[DayForecast]`, `bom_today_url: str`, `bom_7day_url: str`

## 3. Backend — Weather Service

- [x] 3.1 Extend the Open-Meteo request in `backend/app/services/weather.py` to include `daily=temperature_2m_max,temperature_2m_min,weather_code`, `forecast_days=8`, and `timezone=auto`
- [x] 3.2 Extract today's `temp_min` and `temp_max` from `daily` index 0
- [x] 3.3 Build `forecast_7day` list from `daily` indices 1–7: derive single-letter day from date string, round min/max to int
- [x] 3.4 Add `bom_url` parameter to `get_weather` signature; construct `bom_today_url` (`bom_url + "#today"`) and `bom_7day_url` (`bom_url + "#7-days"`) and include in returned `WeatherResponse`

## 4. Backend — Router

- [x] 4.1 Update `backend/app/routers/weather.py` to read `bom_url` from each location in config and pass it to `get_weather`

## 5. Backend — Tests

- [x] 5.1 Update unit tests in `backend/tests/unit/test_weather_service.py` to assert `temp_min`, `temp_max`, `forecast_7day`, `bom_today_url`, `bom_7day_url` are present and correct in the response
- [x] 5.2 Update integration tests in `backend/tests/integration/test_weather_endpoints.py` to reflect the new response shape and the three Victorian locations

## 6. Frontend — WeatherCard Component

- [x] 6.1 Update `WeatherCard.vue` to display today's min and max as integers below the current temperature (e.g. `Min 11° Max 24°`)
- [x] 6.2 Add a compact 7-day forecast row: render each `forecast_7day` entry as a column showing day letter, min, and max
- [x] 6.3 Add two BOM link buttons ("Today" and "7-day") that open `bom_today_url` and `bom_7day_url` in a new tab
- [x] 6.4 Display current temperature as a rounded integer (e.g. `18°C`)

## 7. Frontend — Tests

- [x] 7.1 Update `frontend/src/tests/unit/WeatherCard.spec.js` to cover: today min/max display, 7-day row rendering, BOM links present and target new tab
