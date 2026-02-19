from pydantic import BaseModel


class DayForecast(BaseModel):
    day: str
    temp_min: int
    temp_max: int


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    temp_min: float
    temp_max: float
    forecast_7day: list[DayForecast]
    bom_today_url: str
    bom_7day_url: str
