### Requirement: Three default Victorian locations
The system SHALL serve weather data for exactly three hardcoded locations: Castlemaine, Melbourne, and Sorrento (all Victoria, AU). These locations SHALL be defined in `backend/config.yaml`, each with `city`, `country`, `bom_url`, `fire_district`, and `show_fire_danger` fields.

#### Scenario: All three locations returned
- **WHEN** the client calls `GET /weather/`
- **THEN** the response contains exactly three items, one each for Castlemaine, Melbourne, and Sorrento

#### Scenario: Location config includes BOM URL
- **WHEN** `config.yaml` is loaded
- **THEN** each location entry has a `bom_url` field containing the full base BOM URL for that location

#### Scenario: Location config includes fire_district
- **WHEN** `config.yaml` is loaded
- **THEN** each location entry has a `fire_district` field containing the CFA district name for that location

#### Scenario: Castlemaine has show_fire_danger true
- **WHEN** `config.yaml` is loaded
- **THEN** the Castlemaine entry has `show_fire_danger: true`

#### Scenario: Melbourne and Sorrento have show_fire_danger false
- **WHEN** `config.yaml` is loaded
- **THEN** Melbourne and Sorrento entries have `show_fire_danger: false`

---

### Requirement: Today's minimum and maximum temperature
The API response for each location SHALL include `temp_min` and `temp_max` representing today's forecast minimum and maximum temperature in Celsius, sourced from the `daily` data at index 0 (today) from Open-Meteo.

#### Scenario: Today's min/max present in response
- **WHEN** the weather endpoint returns a location
- **THEN** the response includes `temp_min` (float) and `temp_max` (float) for the current calendar day

#### Scenario: Min is less than or equal to max
- **WHEN** today's forecast data is returned
- **THEN** `temp_min` SHALL be less than or equal to `temp_max`

---

### Requirement: Seven-day daily forecast
The API response SHALL include a `forecast_7day` field containing a list of exactly 7 `DayForecast` objects representing the 7 days starting from tomorrow. Each object SHALL contain:
- `day` (string): single uppercase letter — the first letter of the English weekday name (e.g. "M" for Monday, "T" for Tuesday)
- `temp_min` (int): daily minimum temperature in Celsius, rounded to the nearest integer
- `temp_max` (int): daily maximum temperature in Celsius, rounded to the nearest integer

#### Scenario: Forecast contains 7 entries starting tomorrow
- **WHEN** the weather endpoint returns a location
- **THEN** `forecast_7day` has exactly 7 entries, with the first entry corresponding to tomorrow's date

#### Scenario: Day letter derived from date
- **WHEN** a forecast day falls on a Wednesday
- **THEN** the `day` field for that entry is `"W"`

#### Scenario: Temperature values are integers
- **WHEN** Open-Meteo returns a daily min of 12.7 and max of 23.4
- **THEN** `forecast_7day[i].temp_min` is `13` and `forecast_7day[i].temp_max` is `23`

---

### Requirement: BOM deep-links in response
Each location's API response SHALL include two BOM URL fields:
- `bom_today_url`: the location's `bom_url` from config with `#today` appended
- `bom_7day_url`: the location's `bom_url` from config with `#7-days` appended

#### Scenario: Castlemaine BOM links
- **WHEN** the response for Castlemaine is returned
- **THEN** `bom_today_url` is `https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine#today`
- **AND** `bom_7day_url` is `https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine#7-days`

#### Scenario: Melbourne BOM links
- **WHEN** the response for Melbourne is returned
- **THEN** `bom_today_url` is `https://www.bom.gov.au/location/australia/victoria/central/bvic_pt042-melbourne#today`
- **AND** `bom_7day_url` is `https://www.bom.gov.au/location/australia/victoria/central/bvic_pt042-melbourne#7-days`

#### Scenario: Sorrento BOM links
- **WHEN** the response for Sorrento is returned
- **THEN** `bom_today_url` is `https://www.bom.gov.au/location/australia/victoria/central/o2607452563-sorrento#today`
- **AND** `bom_7day_url` is `https://www.bom.gov.au/location/australia/victoria/central/o2607452563-sorrento#7-days`

---

### Requirement: WeatherCard displays current conditions
The `WeatherCard` component SHALL display the following fields from the weather response:
- Current temperature as a large integer in °C (e.g. `18°C`)
- Today's min and max as integers in °C (e.g. `Min 11° Max 24°`)
- Verbal description (e.g. "Partly cloudy")
- Humidity as a percentage
- Wind speed in km/h

#### Scenario: Current temperature shown as integer
- **WHEN** the API returns `temperature: 17.8`
- **THEN** the card displays `18°C`

#### Scenario: Today min/max shown as integers
- **WHEN** the API returns `temp_min: 11.2` and `temp_max: 23.6`
- **THEN** the card displays `Min 11°` and `Max 24°`

---

### Requirement: WeatherCard displays compact 7-day forecast
The `WeatherCard` component SHALL display a compact 7-day forecast row below the current conditions. Each of the 7 days SHALL show:
- Single uppercase day letter (e.g. `T`)
- Min temperature as an integer in °C
- Max temperature as an integer in °C

The 7 entries SHALL be displayed in a single horizontal row in day order (tomorrow first).

#### Scenario: 7-day row renders all entries
- **WHEN** the card receives `forecast_7day` with 7 entries
- **THEN** all 7 day columns are visible in a single row

#### Scenario: Day letters reflect correct sequence
- **WHEN** today is Thursday
- **THEN** the 7-day row starts with `F` (Friday) and ends with `T` (Thursday)

---

### Requirement: WeatherCard displays BOM links
The `WeatherCard` component SHALL display two links to the official BOM forecast page for the location:
- A link labelled "Today" opening `bom_today_url`
- A link labelled "7-day" opening `bom_7day_url`

Both links SHALL open in a new browser tab.

#### Scenario: BOM links open in new tab
- **WHEN** the user clicks either BOM link
- **THEN** the BOM forecast page opens in a new browser tab

#### Scenario: Both links are visible on each card
- **WHEN** a WeatherCard is rendered with valid BOM URLs
- **THEN** both "Today" and "7-day" links are present on the card

---

### Requirement: Open-Meteo request includes daily forecast data
The weather service SHALL request daily forecast data from Open-Meteo in the same HTTP call as current conditions, using:
- `daily=temperature_2m_max,temperature_2m_min,weather_code`
- `forecast_days=8`
- `timezone=auto`

#### Scenario: Single API call returns both current and daily data
- **WHEN** `get_weather` is called for a location
- **THEN** exactly one HTTP request is made to `api.open-meteo.com` containing both `current` and `daily` parameters

---

### Requirement: WeatherResponse includes fire data fields
Each `WeatherResponse` SHALL include:
- `total_fire_ban` (bool): whether a Total Fire Ban is in effect today for this location's district; `false` if the location has no `fire_district`
- `fire_danger` (list[FireDangerDay] | null): 4-day FDR data if `show_fire_danger` is `true` for this location, otherwise `null`

#### Scenario: total_fire_ban present in all responses
- **WHEN** `GET /api/weather/` returns any location
- **THEN** the response includes a `total_fire_ban` boolean field

#### Scenario: fire_danger present for show_fire_danger locations
- **WHEN** `GET /api/weather/` returns the Castlemaine location
- **THEN** the response includes a `fire_danger` list with 4 entries

#### Scenario: fire_danger null for non-show_fire_danger locations
- **WHEN** `GET /api/weather/` returns Melbourne or Sorrento
- **THEN** `fire_danger` is `null`
