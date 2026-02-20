## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Fire Danger Rating help popup
The `WeatherCard` component SHALL display a `?` icon button next to the Fire Danger Ratings label. Clicking it SHALL open a dialog showing all five AFDRS rating levels as stacked coloured bands, populated from the same `FDR_COLOURS` map used by the badges. Each band SHALL display the rating name using the correct background and text colour for that rating. The dialog SHALL be closeable.

#### Scenario: Help button is present when FDR row is shown
- **WHEN** a `WeatherCard` renders a non-null `fire_danger` list
- **THEN** a `?` button is visible adjacent to the Fire Danger Ratings label

#### Scenario: Help dialog opens on click
- **WHEN** the user clicks the `?` button
- **THEN** a dialog opens showing the fire danger rating scale

#### Scenario: Dialog shows all five AFDRS ratings
- **WHEN** the help dialog is open
- **THEN** it displays bands for No Rating, Moderate, High, Extreme, and Catastrophic

#### Scenario: Dialog bands use FDR_COLOURS values
- **WHEN** the help dialog is open
- **THEN** each band's background colour matches the corresponding entry in `FDR_COLOURS`

#### Scenario: Dialog is closed by default
- **WHEN** a `WeatherCard` is first rendered
- **THEN** the help dialog is not visible
