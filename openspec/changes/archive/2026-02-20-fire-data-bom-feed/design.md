## Context

The current fire service (`fire.py`) fetches the CFA RSS feed and parses HTML-embedded text to extract fire danger ratings and Total Fire Ban status. The CFA RSS feed never includes numeric FBI values — `FireDangerDay.index` is always `null`.

The BOM publishes an XML feed (`https://www.bom.gov.au/fwo/IDV18555.xml`) with clean structured data: `<element type="fire_behaviour_index">` and `<text type="fire_danger">` per district per day. FBI values are always present. District names match those already in `config.yaml`.

However, the BOM feed contains no TFB data. The CFA RSS feed remains the only available source for TFB status.

## Goals / Non-Goals

**Goals:**
- Parse the BOM XML feed to populate `FireDangerDay.index` with numeric FBI values
- Retain the CFA RSS feed as the TFB-only source
- Keep both fetches within the existing single-fetch-per-request architecture

**Non-Goals:**
- Changing the `FireDangerDay` data model
- Changing how TFB is displayed on the frontend
- Making the feed URLs configurable at runtime

## Decisions

**Two feeds, each used for what it provides**
The BOM feed becomes the primary source for FDR ratings and FBI index. The CFA RSS feed is retained solely for TFB status. `parse_fire_xml` is renamed/replaced with `parse_bom_xml`; a separate `parse_cfa_tfb` handles TFB extraction only from the CFA feed. Both are called once per request and their results merged in the router.

Considered alternative: BOM feed only, drop TFB. Rejected — TFB is safety-critical information and worth the second fetch.

**Fetch both feeds concurrently**
Use `asyncio.gather` (already available via httpx async client) to fetch both feeds in parallel, keeping latency impact minimal.

Considered alternative: fetch sequentially. Rejected — adds unnecessary latency for an independent request.

**Retain district name matching as-is**
The BOM feed uses `description` attributes (e.g. "North Central", "Central") that match `config.yaml` district names exactly. No mapping table needed.

**Keep `fire.py` as the single fire module**
Both parsers live in `fire.py`. A single `fetch_fire_data()` function returns the merged result keyed by district, preserving the interface consumed by `weather.py`.

## Risks / Trade-offs

- **BOM feed is unofficial** → No SLA or guaranteed stability. If the feed changes structure or disappears, ratings and FBI go dark. TFB would still work via CFA. Mitigation: graceful degradation already in place (empty dict on error).
- **Two network requests instead of one** → Concurrent fetch keeps this acceptable. Mitigation: `asyncio.gather` with independent timeouts.
- **CFA feed HTML parsing is fragile** → Already a known risk; unchanged by this design. Future work: find a cleaner TFB source.
- **District name mismatches** → BOM uses `description` attribute; if BOM ever renames a district, matching silently fails. Mitigation: existing fallback to `false`/`null` is safe.

## Migration Plan

1. Add `parse_bom_xml()` alongside existing `parse_fire_xml()` in `fire.py`
2. Update `fetch_fire_data()` to fetch both feeds concurrently and merge results
3. Update unit tests with BOM sample XML; FBI index assertions now non-null
4. Remove `parse_fire_xml()` once new parser is verified
