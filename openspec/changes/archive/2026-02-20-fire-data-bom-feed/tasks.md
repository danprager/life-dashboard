## 1. BOM Feed Parser

- [x] 1.1 Add `parse_bom_xml(xml_data)` to `fire.py` — parse `<area type="fire-district">` blocks, extract `fire_behaviour_index` and `fire_danger` per district per day (4 days)
- [x] 1.2 Return dict keyed by district name: `{ district: [FireDangerDay, ...] }`
- [x] 1.3 Handle parse errors gracefully — return `{}` on malformed XML

## 2. CFA TFB-only Parser

- [x] 2.1 Extract TFB parsing from `parse_fire_xml()` into a standalone `parse_cfa_tfb(xml_data)` function
- [x] 2.2 Return dict keyed by district name: `{ district: bool }`
- [x] 2.3 Handle parse errors gracefully — return `{}`

## 3. Concurrent Fetch

- [x] 3.1 Update `fetch_fire_data()` to fetch both feeds concurrently using `asyncio.gather` (or threading if keeping stdlib-only)
- [x] 3.2 Merge results: combine BOM ratings/FBI with CFA TFB into the existing `{ district: { total_fire_ban, fire_danger } }` interface
- [x] 3.3 Ensure each feed failure degrades independently (BOM failure → `fire_danger: null`; CFA failure → `total_fire_ban: false`)

## 4. Tests

- [x] 4.1 Add unit tests for `parse_bom_xml()` using sample BOM XML — assert correct district names, ratings, and FBI index values
- [x] 4.2 Add unit test asserting `parse_bom_xml()` returns `{}` on malformed XML
- [x] 4.3 Add unit tests for `parse_cfa_tfb()` using sample CFA XML — assert correct TFB values per district
- [x] 4.4 Update existing `test_fire_service.py` tests that reference the old `parse_fire_xml()` interface
- [x] 4.5 Add integration test asserting `FireDangerDay.index` is a non-null integer when BOM feed is available

## 5. Scale Panel FBI Ranges (TDD)

- [x] 5.1 Write failing tests asserting each rating band in the help panel shows its FBI range label:
  - No Rating: `< 12`
  - Moderate: `12–23`
  - High: `24–49`
  - Extreme: `50–99`
  - Catastrophic: `≥ 100`
- [x] 5.2 Run tests — confirm they fail (red)
- [x] 5.3 Add `fbi` range string to each entry in `FDR_COLOURS` in `WeatherCard.vue`
- [x] 5.4 Update the help panel bands to display the FBI range alongside the rating name
- [x] 5.5 Run tests — confirm they pass (green)

## 6. Cleanup

- [x] 5.1 Remove `parse_fire_xml()` once new parsers are verified by tests
- [x] 5.2 Run `pytest backend/tests/` — all tests pass
