## ADDED Requirements

### Requirement: FBI range displayed in fire danger rating scale panel
The help panel SHALL display the FBI index range for each AFDRS rating level alongside the rating name, sourced from the official AFDRS thresholds:

| Rating | FBI Range |
|---|---|
| No Rating | < 12 |
| Moderate | 12–23 |
| High | 24–49 |
| Extreme | 50–99 |
| Catastrophic | ≥ 100 |

#### Scenario: No Rating band shows FBI range
- **WHEN** the help panel is open
- **THEN** the No Rating band displays `< 12`

#### Scenario: Moderate band shows FBI range
- **WHEN** the help panel is open
- **THEN** the Moderate band displays `12–23`

#### Scenario: High band shows FBI range
- **WHEN** the help panel is open
- **THEN** the High band displays `24–49`

#### Scenario: Extreme band shows FBI range
- **WHEN** the help panel is open
- **THEN** the Extreme band displays `50–99`

#### Scenario: Catastrophic band shows FBI range
- **WHEN** the help panel is open
- **THEN** the Catastrophic band displays `≥ 100`

---

## MODIFIED Requirements

### Requirement: CFA RSS feed fetched once per request
The backend SHALL fetch both fire data feeds at most once per incoming `/api/weather/` request, share results across all location responses, and fetch them concurrently:

- **BOM XML feed** (`https://www.bom.gov.au/fwo/IDV18555.xml`) — source for fire danger ratings and numeric FBI values per district per day
- **CFA RSS feed** (`https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml`) — source for Total Fire Ban status per district

Both fetches SHALL use Python stdlib only (`urllib.request` and `xml.etree.ElementTree`). If either feed is unreachable or returns malformed data, the backend SHALL degrade gracefully: TFB defaults to `false` and `fire_danger` defaults to `null`.

#### Scenario: Both feeds fetched once per request
- **WHEN** `GET /api/weather/` is called
- **THEN** exactly one HTTP request is made to the BOM XML feed URL
- **AND** exactly one HTTP request is made to the CFA RSS feed URL

#### Scenario: BOM feed errors degrade gracefully
- **WHEN** the BOM feed is unreachable or returns malformed XML
- **THEN** the weather endpoint still returns a valid response for all locations
- **AND** `fire_danger` is `null` for all locations

#### Scenario: CFA feed errors degrade gracefully
- **WHEN** the CFA RSS feed is unreachable or returns malformed XML
- **THEN** the weather endpoint still returns a valid response for all locations
- **AND** `total_fire_ban` is `false` for all locations

---

### Requirement: 4-day Fire Danger Rating data for show_fire_danger locations
For locations with `show_fire_danger: true`, the backend SHALL populate `fire_danger` in `WeatherResponse` with a list of exactly 4 `FireDangerDay` objects: today plus the next 3 days, in chronological order, sourced from the BOM XML feed for that location's district.

Each `FireDangerDay` SHALL contain:
- `day` (string): single uppercase letter — first letter of the English weekday name
- `rating` (string): fire danger rating label from the BOM feed (e.g. "High", "Extreme", "Catastrophic")
- `index` (int | null): numeric Fire Behaviour Index from the BOM feed; `null` only if absent from feed

For locations with `show_fire_danger: false`, `fire_danger` SHALL be `null`.

#### Scenario: Castlemaine receives 4-day FDR data
- **WHEN** `GET /api/weather/` is called
- **AND** Castlemaine has `show_fire_danger: true`
- **THEN** Castlemaine's response has `fire_danger` as a list of exactly 4 entries
- **AND** the first entry corresponds to today's date

#### Scenario: Melbourne and Sorrento have null fire_danger
- **WHEN** `GET /api/weather/` is called
- **AND** Melbourne has `show_fire_danger: false`
- **THEN** Melbourne's response has `fire_danger: null`

#### Scenario: Day letter format
- **WHEN** a FireDangerDay falls on a Wednesday
- **THEN** its `day` field is `"W"`

#### Scenario: FBI index populated from BOM feed
- **WHEN** the BOM feed includes a `fire_behaviour_index` value of `36` for a day
- **THEN** `FireDangerDay.index` is `36`
