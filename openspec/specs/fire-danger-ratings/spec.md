### Requirement: CFA RSS feed fetched once per request
The backend SHALL fetch the CFA fire danger RSS feed (`https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml`) at most once per incoming `/api/weather/` request, parse it, and share the results across all location responses. The fetch SHALL use Python stdlib only (`urllib.request` and `xml.etree.ElementTree`).

#### Scenario: Single fetch per request
- **WHEN** `GET /api/weather/` is called
- **THEN** exactly one HTTP request is made to the CFA RSS feed URL

#### Scenario: Feed parse errors are handled gracefully
- **WHEN** the CFA feed is unreachable or returns malformed XML
- **THEN** the weather endpoint still returns a valid response for all locations
- **AND** `total_fire_ban` is `false` and `fire_danger` is `null` for all locations

---

### Requirement: Total Fire Ban indicator on all configured cards
For each location that has a `fire_district` configured, the backend SHALL set `total_fire_ban: true` in the `WeatherResponse` if the CFA feed declares a Total Fire Ban for that district on the current day. If no TFB is declared, `total_fire_ban` SHALL be `false`.

#### Scenario: TFB declared for district
- **WHEN** the CFA feed declares a Total Fire Ban for the "North Central" district
- **AND** Castlemaine has `fire_district: North Central`
- **THEN** Castlemaine's `WeatherResponse` has `total_fire_ban: true`

#### Scenario: TFB not declared
- **WHEN** the CFA feed does not declare a TFB for a location's district
- **THEN** that location's `WeatherResponse` has `total_fire_ban: false`

#### Scenario: Location without fire_district
- **WHEN** a location has no `fire_district` in config
- **THEN** its `WeatherResponse` has `total_fire_ban: false` and `fire_danger: null`

---

### Requirement: 4-day Fire Danger Rating data for show_fire_danger locations
For locations with `show_fire_danger: true`, the backend SHALL populate `fire_danger` in `WeatherResponse` with a list of exactly 4 `FireDangerDay` objects: today plus the next 3 days, in chronological order, sourced from the CFA RSS feed for that location's district.

Each `FireDangerDay` SHALL contain:
- `day` (string): single uppercase letter — first letter of the English weekday name
- `rating` (string): CFA rating label (e.g. "High", "Extreme", "Catastrophic")
- `index` (int | null): numeric Fire Danger Index if present in feed, otherwise `null`

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

#### Scenario: FDI index present in feed
- **WHEN** the CFA feed includes a numeric FDI for a day
- **THEN** `FireDangerDay.index` is that integer value

#### Scenario: FDI index absent from feed
- **WHEN** the CFA feed does not include a numeric FDI for a day
- **THEN** `FireDangerDay.index` is `null`

---

### Requirement: TFB banner displayed below temperature block on all cards
The `WeatherCard` component SHALL display a Total Fire Ban warning row immediately below the temperature block when `total_fire_ban` is `true`. When `total_fire_ban` is `false`, no TFB indicator SHALL be shown.

The banner SHALL use a red background (`#e8260b`) with white text and read "TOTAL FIRE BAN".

#### Scenario: TFB banner appears when total_fire_ban is true
- **WHEN** a `WeatherCard` receives `total_fire_ban: true`
- **THEN** a "TOTAL FIRE BAN" banner is visible below the temperature block

#### Scenario: TFB banner absent when total_fire_ban is false
- **WHEN** a `WeatherCard` receives `total_fire_ban: false`
- **THEN** no TFB banner is rendered on the card

#### Scenario: TFB banner uses official red colour
- **WHEN** the TFB banner is rendered
- **THEN** it has a background colour of `#e8260b` and white text

---

### Requirement: 4-day FDR row with official CFA colour coding
The `WeatherCard` component SHALL display a compact 4-day FDR row when `fire_danger` is non-null. Each day SHALL show:
- Single uppercase day letter
- A coloured block containing the rating word, using the official AFDRS colour for that rating
- The numeric FDI index below the block (omitted if `null`)

The FDR row SHALL NOT be rendered when `fire_danger` is `null`.

Official AFDRS colours (sampled from CFA reference image `fire-ratings.png`):
| Rating | Background | Text |
|---|---|---|
| No Rating | `#FFFFFF` | black |
| Moderate | `#6DB840` | white |
| High | `#F7D94A` | black |
| Extreme | `#E87820` | white |
| Catastrophic | `#922B21` | white |

Any rating string not in this table SHALL fall back to `#888888` with white text.

#### Scenario: FDR row shown when fire_danger is non-null
- **WHEN** a `WeatherCard` receives a non-null `fire_danger` list
- **THEN** the FDR row is rendered with 4 day columns

#### Scenario: FDR row hidden when fire_danger is null
- **WHEN** a `WeatherCard` receives `fire_danger: null`
- **THEN** no FDR row is rendered

#### Scenario: Moderate badge is green
- **WHEN** a day's rating is "Moderate"
- **THEN** the rating badge background is `#6DB840`

#### Scenario: High badge is yellow
- **WHEN** a day's rating is "High"
- **THEN** the rating badge background is `#F7D94A`

#### Scenario: Extreme badge is orange
- **WHEN** a day's rating is "Extreme"
- **THEN** the rating badge background is `#E87820`

#### Scenario: Catastrophic badge is dark red
- **WHEN** a day's rating is "Catastrophic"
- **THEN** the rating badge background is `#922B21`

#### Scenario: No Rating badge is white with black text
- **WHEN** a day's rating is "No Rating"
- **THEN** the rating badge background is `#FFFFFF` and text colour is black

#### Scenario: Unknown rating falls back to grey
- **WHEN** a day's rating is not one of the five AFDRS levels
- **THEN** the rating badge background is `#888888`

#### Scenario: FDI index shown when present
- **WHEN** a `FireDangerDay` has `index: 87`
- **THEN** the value `87` is displayed below the rating block

#### Scenario: FDI index omitted when null
- **WHEN** a `FireDangerDay` has `index: null`
- **THEN** no index value is rendered for that day

---

### Requirement: Fire Danger Rating help popup
The `WeatherCard` component SHALL display a "Scale" button next to the Fire Danger Ratings label. Clicking it SHALL open a panel showing all five AFDRS rating levels as stacked coloured bands, populated from the same `FDR_COLOURS` map used by the badges. Each band SHALL display the rating name using the correct background and text colour for that rating. The panel SHALL be toggleable.

#### Scenario: Scale button is present when FDR row is shown
- **WHEN** a `WeatherCard` renders a non-null `fire_danger` list
- **THEN** a "Scale" button is visible adjacent to the Fire Danger Ratings label

#### Scenario: Help panel opens on click
- **WHEN** the user clicks the "Scale" button
- **THEN** a panel opens showing the fire danger rating scale

#### Scenario: Panel shows all five AFDRS ratings
- **WHEN** the help panel is open
- **THEN** it displays bands for No Rating, Moderate, High, Extreme, and Catastrophic

#### Scenario: Panel bands use FDR_COLOURS values
- **WHEN** the help panel is open
- **THEN** each band's background colour matches the corresponding entry in `FDR_COLOURS`

#### Scenario: Panel is closed by default
- **WHEN** a `WeatherCard` is first rendered
- **THEN** the help panel is not visible
