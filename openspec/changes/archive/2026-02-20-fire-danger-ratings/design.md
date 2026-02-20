## Context

The dashboard currently shows weather for 3 Victorian locations (Castlemaine, Melbourne, Sorrento). Victoria is a high fire-risk state. The CFA publishes a live RSS feed (`https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml`) with 5-day Fire Danger Ratings and Total Fire Ban status per district, updated daily. No API key or registration is required.

Current state: `WeatherResponse` has no fire-related fields. `WeatherCard.vue` has no fire UI. Each location in `config.yaml` is a flat dict with `city`, `country`, and `bom_url`.

Each Victorian location belongs to a CFA fire district (e.g. Castlemaine → "North Central", Melbourne → "Central"). The feed uses district names as identifiers.

### Per-card configurability

Cards are not uniform — different locations have different information needs. This change introduces the first instance of **per-location display configuration**: a location can opt in or out of showing fire danger data. This is a deliberate design pattern that should be extended as the dashboard grows (e.g. tides for coastal locations, UV index, etc.). Configuration lives in `config.yaml` alongside the location definition, not in frontend code.

## Goals / Non-Goals

**Goals:**
- Show a Total Fire Ban warning below the temperature block on all 3 cards when a TFB is declared for that card's district
- Show a 4-day FDR row (today + 3 days) on the Castlemaine card only, using official CFA colour coding with rating word and FDI index
- Parse the CFA RSS feed with Python stdlib only (no new dependencies)
- Keep fire data fetched once per `/api/weather/` call, not per location

**Non-Goals:**
- Fire data for non-Victorian locations
- Push notifications or alerts
- Historical fire data
- Caching the CFA feed between requests (can be added later)

## Decisions

### 1. Parse CFA RSS with stdlib `urllib` + `xml.etree.ElementTree`

The CFA feed is a standard RSS 2.0 XML document. Python's stdlib handles both the fetch (`urllib.request`) and parse (`xml.etree.ElementTree`). No new packages needed.

**Alternative considered:** `httpx` (already used for weather). Avoided to keep the fire service self-contained and synchronous — the feed is small and latency is not critical.

### 2. Fetch fire data once per request, shared across locations

`weather.py` calls `fire.py` once to get a `FireData` object (a dict of district → `FireDistrictData`), then passes relevant slices to each location's `WeatherResponse`. This avoids 3 duplicate HTTP requests to the CFA feed.

**Alternative considered:** Each location fetches its own fire data. Rejected — wasteful and slower.

### 3. Per-location display config in `config.yaml`

Each location entry in `config.yaml` can carry optional display flags that control what information its card shows. This change introduces two fire-specific fields:

- `fire_district`: string matching a CFA district name in the RSS feed (required for any fire data)
- `show_fire_danger`: boolean — if `true`, the 4-day FDR row is populated and shown on the card

Current config intent:

| Location | `fire_district` | `show_fire_danger` |
|---|---|---|
| Castlemaine | North Central | `true` |
| Melbourne | Central | `false` |
| Sorrento | Central | `false` |

Melbourne and Sorrento still get `total_fire_ban` status (because they have `fire_district`), but do not show the FDR row. A location with no `fire_district` gets neither.

This pattern is the foundation for future per-card configurability (tides, UV index, etc.) — the config drives what the backend computes and what the frontend renders.

### 4. `FireDangerDay` model with `day`, `rating`, `index`

- `day`: single uppercase letter (first letter of weekday name)
- `rating`: string matching CFA label (e.g. "High", "Extreme", "Catastrophic")
- `index`: `int | None` — FDI numeric value if present in feed, else `null`

### 5. Official CFA colour coding in frontend

CFA ratings map to specific colours used in their public materials:

| Rating | Colour |
|---|---|
| No Rating | grey |
| Low-Moderate | `#3d9ad6` (blue) |
| High | `#f5a623` (orange) |
| Very High | `#e07020` (dark orange) |
| Severe | `#e8260b` (red) |
| Extreme | `#c8003a` (dark red) |
| Catastrophic | `#2d0000` (near black, white text) |

TFB banner: red background (`#e8260b`), white text.

### 6. FDR row layout: day letter + coloured block with word rating + FDI index below

Each day column shows:
```
  T
█ EXTREME █
   87
```
Index is omitted (not rendered) if `null`.

## Risks / Trade-offs

- **CFA feed structure may change** → Mitigation: parse defensively, return `null` fire data rather than crashing; log parse errors.
- **District name mismatch** → The feed uses exact district names. If config district string doesn't match a feed entry, fire data silently returns `null` for that location. Mitigation: exact string match with a clear config comment.
- **Feed unavailability** → Mitigation: catch network errors in `fire.py`, return empty `FireData`; weather response still succeeds with `total_fire_ban: false` and `fire_danger: null`.
- **Feed latency adds to weather response time** → Acceptable for a dashboard with a manual refresh. Can add caching later.

## Migration Plan

1. Update `config.yaml` with `fire_district` and `show_fire_danger` per location
2. Add `FireDangerDay` to `models/weather.py`; extend `WeatherResponse`
3. Create `services/fire.py`
4. Update `services/weather.py` to call fire service and attach results
5. Update `WeatherCard.vue` with TFB banner and FDR row

No database changes. No breaking API changes for existing consumers (new fields added, none removed). Deploy is a straight Render push.

## Open Questions

- As more per-card data types are added (tides, UV, etc.), `config.yaml` may benefit from a nested `display:` block per location rather than flat flags. Not needed now — revisit when a second configurable data type is added.
