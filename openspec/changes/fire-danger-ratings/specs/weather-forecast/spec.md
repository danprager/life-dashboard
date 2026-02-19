## MODIFIED Requirements

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

## ADDED Requirements

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
