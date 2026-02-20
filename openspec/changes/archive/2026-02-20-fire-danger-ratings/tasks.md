## 1. Config

- [x] 1.1 Add `fire_district` and `show_fire_danger` fields to all 3 locations in `backend/config.yaml`

## 2. Data Model

- [x] 2.1 Add `FireDangerDay` Pydantic model (`day`, `rating`, `index`) to `backend/app/models/weather.py`
- [x] 2.2 Add `total_fire_ban: bool` and `fire_danger: list[FireDangerDay] | None` to `WeatherResponse`

## 3. Fire Service

- [x] 3.1 Create `backend/app/services/fire.py` — fetch CFA RSS feed with `urllib.request`
- [x] 3.2 Parse feed XML with `xml.etree.ElementTree` to extract TFB status and 5-day FDR per district
- [x] 3.3 Return a dict of district → fire data; handle network errors and malformed XML gracefully (return empty dict)

## 4. Weather Service Integration

- [x] 4.1 In `backend/app/services/weather.py`, call fire service once before the location loop
- [x] 4.2 Pass `total_fire_ban` and `fire_danger` (or `null`) to each `WeatherResponse` based on config flags

## 5. Frontend — TFB Banner

- [x] 5.1 In `WeatherCard.vue`, add a TFB banner below the temperature block, visible only when `total_fire_ban` is `true`
- [x] 5.2 Style banner: red background (`#e8260b`), white text, reads "TOTAL FIRE BAN"

## 6. Frontend — FDR Row

- [x] 6.1 In `WeatherCard.vue`, add a 4-day FDR row rendered only when `fire_danger` is non-null
- [x] 6.2 Each day column: single letter day, coloured block with rating word, FDI index below (omitted if null)
- [x] 6.3 Apply official CFA colour mapping to rating blocks (7 rating levels)

## 7. Tests

- [x] 7.1 Add unit tests for `fire.py` — verify TFB parsing and FDR extraction from sample XML
- [x] 7.2 Update `WeatherCard` component tests to cover TFB banner (shown/hidden) and FDR row (shown/hidden)
