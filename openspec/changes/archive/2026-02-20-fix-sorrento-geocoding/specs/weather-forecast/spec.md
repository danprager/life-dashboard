## MODIFIED Requirements

### Requirement: Location resolution supports explicit coordinates
When a location in `config.yaml` has `latitude` and `longitude` fields, the backend SHALL use those coordinates directly and skip the geocoding API call.

#### Scenario: Pinned coordinates bypass geocoding
- **WHEN** a location has `latitude` and `longitude` in config
- **THEN** no geocoding API request is made
- **AND** the provided coordinates are used for the weather fetch

#### Scenario: Display name from config
- **WHEN** coordinates are pinned and `name` is set in config
- **THEN** `WeatherResponse.location` uses the config name

#### Scenario: Geocoding still used when coordinates absent
- **WHEN** a location has no `latitude`/`longitude` in config
- **THEN** the geocoding API is called as before
