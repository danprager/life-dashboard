## Context

`WeatherCard.vue` contains a `FDR_COLOURS` map that assigns hex colours to fire danger rating strings. The current map is wrong — Moderate is blue, Extreme is red, Catastrophic is near-black — and includes three legacy ratings (Low-Moderate, Very High, Severe) that predate the 2022 AFDRS simplification.

The official AFDRS palette has five levels and is visible in `fire-ratings.png` (CFA source). Exact hex values will be sampled from that image.

## Goals / Non-Goals

**Goals:**
- Replace all five colour values with the official AFDRS colours
- Fix No Rating: white background with dark (black) text
- Remove legacy ratings from the map (Low-Moderate, Very High, Severe)
- Add unit tests that assert each rating's colour explicitly

**Non-Goals:**
- Changing the rating strings returned by the CFA RSS feed
- Changing the FDR row layout or structure
- Addressing legacy ratings that may still appear in the feed (they fall through to the existing grey fallback)

## Decisions

**Sample hex values from `fire-ratings.png`**
The reference image is from the official CFA page and shows the exact rendered colours. Sampling directly from the image is more reliable than guessing or sourcing from a PDF style guide that wasn't accessible.

**Remove legacy ratings from the map**
Low-Moderate, Very High, and Severe are not part of the current AFDRS. There is no confirmed evidence the live CFA feed still emits them. Removing them keeps the map honest; the existing `?? '#888888'` fallback handles any unexpected value gracefully.

**Test colours via rendered inline style**
`fdrColour()` is a private function inside the component. Tests will mount the component with controlled `fire_danger` data and assert the `backgroundColor` inline style on the `.fdr-badge` element — consistent with how the existing test suite exercises the component.

**Black text on No Rating**
No Rating is white — white text on white is invisible. Switch text colour to black for this level only; all others keep white text.

## Risks / Trade-offs

- **Sampled hex values may not be pixel-perfect** → Acceptable; the goal is correctness at the level a user recognises (green/yellow/orange/dark-red), not brand-exact reproduction.
- **Legacy ratings silently fall back to grey** → Acceptable short-term; if the feed ever emits them again, grey is visually neutral and won't mislead.
