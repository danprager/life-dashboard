## Context

Open-Meteo's geocoding API ignores the `country` parameter, returning the highest-population global match. "Sorrento" resolved to Sorrento, Italy rather than Sorrento, Victoria.

## Goals / Non-Goals

**Goals:** Ensure all configured locations resolve to the correct coordinates.
**Non-goals:** Fix geocoding in general; the API bypass is sufficient for a fixed config.

## Decisions

**Pin coordinates in config.yaml, bypass geocoding when present.**
- Alternatives considered: filter by country in app code (not possible — API returns one result); use a different geocoding API (adds dependency).
- Chosen approach is simple, reliable, and makes coordinates explicit and auditable.

**Keep geocoding path for locations without coordinates** (backwards compatible, useful for future additions).

## Implementation

- `config.yaml`: add `latitude`/`longitude` to all three locations
- `weather.py`: if `latitude`/`longitude` provided, skip geocode call; use `location_name` from config for display
- `routers/weather.py`: pass `latitude`, `longitude`, `location_name` from loc config to `get_weather()`

## Risks / Trade-offs

- Coordinates are static — if a location moves (unlikely) config must be updated manually.
- No risk of regression: geocode path unchanged for locations without coordinates.
