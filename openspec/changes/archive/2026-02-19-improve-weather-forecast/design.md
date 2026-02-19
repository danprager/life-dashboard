## Context

The existing weather feature fetches current conditions (temperature, description, humidity, wind) for a single location (Sydney) via Open-Meteo's `/forecast` endpoint with `current` params only. The `WeatherResponse` Pydantic model is returned as a list by the `/weather/` endpoint, and rendered by `WeatherCard.vue` in the dashboard.

The change replaces the Sydney default with three fixed Victorian locations (Castlemaine, Melbourne, Sorrento) and enriches each response with today's min/max, a 7-day daily forecast starting tomorrow, and static BOM deep-links.

## Goals / Non-Goals

**Goals:**
- 3 hardcoded locations in `config.yaml`, each carrying its static BOM URL base
- Backend returns today's min/max and 7 days of daily forecasts (date, single-letter day, min, max)
- `WeatherCard` renders: current temp, today min/max, description, humidity, wind, compact 7-day row, two BOM links
- BOM links use `#today` and `#7-days` anchors appended to each location's base URL

**Non-Goals:**
- Dynamic or user-configurable locations (future work)
- Hourly forecasts
- Weather icons / WMO icon mapping beyond existing text descriptions
- Caching or rate-limiting the Open-Meteo calls

## Decisions

### 1. BOM URLs stored in `config.yaml`, not hardcoded in source

Each location entry gains a `bom_url` field (base URL without anchor). The service reads it and the router passes it through to the response. This keeps location-specific data together and makes future location changes a config-only edit.

Alternative: hardcode in the service or a constants file — rejected because it scatters location metadata across files.

### 2. Single Open-Meteo call per location (combined `current` + `daily`)

Open-Meteo supports combining `current` and `daily` params in one request. We extend the existing call with:
```
daily=temperature_2m_max,temperature_2m_min,weather_code
forecast_days=8
```
This returns today (index 0) plus 7 future days (indices 1–7).

Alternative: two separate requests — rejected as unnecessary overhead.

### 3. Today's min/max comes from `daily[0]`, not current conditions

Open-Meteo's `current` block does not include daily min/max. Index 0 of the `daily` arrays is always today's date.

### 4. 7-day forecast slice: indices 1–7 (tomorrow through +7 days)

The card shows 7 days starting tomorrow. We derive the single-letter day label from each `daily.time[i]` date string (ISO 8601) using Python's `datetime.strptime` → `.strftime("%A")[0]`. This gives M T W T F S S. Positional context (left-to-right sequence) disambiguates the T/T and S/S collisions — no tooltip or suffix needed for this compact display.

### 5. `forecast_7day` as a typed list on the response model

A new `DayForecast` sub-model (`day: str`, `temp_min: float`, `temp_max: float`) is added to `models/weather.py`. `WeatherResponse` carries `forecast_7day: list[DayForecast]`. This keeps the API contract explicit and Pydantic-validated.

Alternative: untyped `list[dict]` — rejected for lack of schema clarity.

### 6. `WeatherCard` layout: two sections

- **Top section**: large current temp, description, today min/max, humidity, wind (retains existing fields)
- **Bottom section**: compact 7-day row (day letter + min/max stacked or inline), then two BOM link buttons

Humidity and wind are retained on the card per requirement.

## Risks / Trade-offs

- **Open-Meteo `daily` timezone**: must pass `timezone=auto` (already done for `current`) so that day boundaries align with local time. Without it, daily indices may be off by one. → Mitigation: confirm `timezone=auto` is included in the extended request params.
- **`forecast_days=8` vs default**: Open-Meteo defaults to 7 days. We need 8 (today + 7 ahead). → Mitigation: explicitly pass `forecast_days=8`.
- **Breaking API change**: removing `humidity`/`wind_speed` was considered but reversed — they are retained. The only breaking aspect is the addition of required new fields, which only affects any consumers beyond the frontend (none currently).
- **T/S day letter collision**: single-letter abbreviation is ambiguous in isolation but unambiguous in a positional sequence starting from a known day. Acceptable for this compact display.

## Migration Plan

1. Update `config.yaml`: replace Sydney entry with 3 Victorian locations + `bom_url` per entry
2. Extend `WeatherResponse` and add `DayForecast` model
3. Update `weather.py` service: extend Open-Meteo params, build `forecast_7day`, attach BOM URLs
4. Update router to pass `bom_url` from config through to service/response
5. Update `WeatherCard.vue`: new layout sections
6. Update unit and integration tests to match new model fields

No database or deployment migration required — all changes are in application code and config.

## Open Questions

- Should `temp_min`/`temp_max` on the card display as integers (rounded) or one decimal place? Assumption: integers (consistent with how current temp is already displayed without decimals).
