## Why

The Open-Meteo geocoding API does not support a `country` filter — the `country` parameter passed in `weather.py` is silently ignored. Searching by city name alone returns the top global result, so "Sorrento" resolves to Sorrento, Italy rather than Sorrento, Victoria. The dashboard is currently showing Italian weather for a Victorian location.

## What Changes

- Add optional `latitude` and `longitude` fields to each location entry in `config.yaml`
- When coordinates are present, skip the geocoding API call and use them directly
- Set coordinates for all three locations (Castlemaine, Melbourne, Sorrento)
- Remove the unused `country` field, or retain it for documentation only

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `weather-forecast`: location resolution now supports explicit coordinates in config, bypassing geocoding when provided

## Impact

- `backend/config.yaml` — add `latitude`/`longitude` to all three locations
- `backend/app/services/weather.py` — skip geocode step when coordinates supplied
- `backend/tests/` — update or add tests covering the coordinate bypass path
