## Why

The current fire data source (CFA RSS feed) does not include numeric Fire Behaviour Index (FBI) values — the `index` field in `FireDangerDay` is always `null`. The unofficial BOM XML feed (`https://www.bom.gov.au/fwo/IDV18555.xml`) provides both the FBI numeric value and the rating label in clean structured XML, keyed by district and day. Switching to this feed unblocks displaying the FBI number on the dashboard.

## What Changes

- Replace the CFA RSS feed fetch and parser in `fire.py` with a parser for the BOM XML feed (`IDV18555.xml`)
- Extract `<element type="fire_behaviour_index">` (numeric FBI) and `<text type="fire_danger">` (rating label) per district per day
- Populate `FireDangerDay.index` with the FBI value (currently always `null`)
- District names in the BOM feed match those already used in `config.yaml` (e.g. "North Central", "Central")
- Total Fire Ban data is not present in this feed — assess whether to retain the CFA RSS feed as a secondary source for TFB only, or drop TFB if BOM feed covers the key use case

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `fire-danger-ratings`: fire data now sourced from BOM XML feed; FBI numeric index populated

## Impact

- `backend/app/services/fire.py` — replace CFA RSS fetch/parse with BOM XML fetch/parse
- `backend/tests/unit/test_fire_service.py` — update sample XML and assertions for new feed format
- `backend/config.yaml` — may need `bom_fire_url` or similar if feed URL is configurable
