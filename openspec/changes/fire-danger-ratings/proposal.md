## Why

Castlemaine is in a high fire-risk area of Victoria. The dashboard should surface Fire Danger Ratings for the coming days alongside weather, and flag Total Fire Bans across all locations when declared.

## What Changes

- Add `fire_district` and `show_fire_danger` fields to each location in `backend/config.yaml`
- Add a new backend service that fetches and parses the CFA RSS feed (`https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml`)
- Extend `WeatherResponse` with:
  - `total_fire_ban: bool` — whether a TFB is in effect today for this location's district (all cards)
  - `fire_danger: list[FireDangerDay] | None` — today + next 3 days of FDR, only for locations with `show_fire_danger: true` (Castlemaine only)
- `FireDangerDay` contains: `day` (single letter), `rating` (e.g. "High", "Extreme"), `index` (numeric FDI if available in feed)
- Update `WeatherCard.vue`:
  - All cards: show a Total Fire Ban banner/badge when `total_fire_ban` is true
  - Castlemaine card only: show a compact 4-day FDR row using official CFA colour coding

## Capabilities

### New Capabilities
- `fire-danger-ratings`: CFA fire danger data per location — TFB indicator on all cards, 4-day FDR row on Castlemaine card, using official colour coding

### Modified Capabilities
- `weather-forecast`: `WeatherResponse` extended with `total_fire_ban` and `fire_danger` fields

## Impact

- **`backend/config.yaml`**: add `fire_district` and `show_fire_danger` per location
- **`backend/app/models/weather.py`**: add `FireDangerDay` model; add `total_fire_ban: bool` and `fire_danger: list[FireDangerDay] | None` to `WeatherResponse`
- **`backend/app/services/fire.py`** (new): fetch CFA RSS XML, parse TFB status and FDR by district
- **`backend/app/services/weather.py`**: call fire service and attach results to `WeatherResponse`
- **`frontend/src/components/WeatherCard.vue`**: TFB banner for all cards; FDR row with official colours for Castlemaine
- No new dependencies — Python standard library handles RSS fetch and XML parse
