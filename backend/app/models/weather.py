from pydantic import BaseModel


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
