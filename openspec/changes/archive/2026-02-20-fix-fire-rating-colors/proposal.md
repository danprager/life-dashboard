## Why

The `fire-danger-ratings` spec codifies incorrect colours — Moderate is missing entirely, and the remaining colours do not match the official AFDRS palette. The dashboard currently shows blue for Moderate, red for Extreme, and near-black for Catastrophic. Users familiar with the official CFA colour scheme will find this confusing and potentially alarming.

## What Changes

- Correct the colour table in the `fire-danger-ratings` spec to reflect the official AFDRS five-level palette (colours by name; hex values sampled from the official CFA reference image):
  - No Rating: white with dark text
  - Moderate: green
  - High: yellow
  - Extreme: orange
  - Catastrophic: dark red
- Update `FDR_COLOURS` in `WeatherCard.vue` to match
- Add unit tests asserting the correct colour for each of the five AFDRS ratings — demonstrating that all colours are correct

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `fire-danger-ratings`: colour table requirements are wrong and must be replaced with the official AFDRS five-level palette

## Impact

- `openspec/changes/fire-danger-ratings/specs/fire-danger-ratings/spec.md` — replace colour table
- `frontend/src/components/WeatherCard.vue` — `FDR_COLOURS` map and badge text colour
- `frontend/src/tests/unit/WeatherCard.spec.js` — add colour assertion tests for all five ratings
