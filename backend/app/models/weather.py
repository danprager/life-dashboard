from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class DayForecast(BaseModel):
    day: str
    temp_min: int
    temp_max: int


class FireDangerDay(BaseModel):
    day: str
    rating: str
    index: Optional[int] = None


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    temp_min: float
    temp_max: float
    forecast_7day: List[DayForecast]
    bom_today_url: str
    bom_7day_url: str
    total_fire_ban: bool = False
    fire_danger: Optional[List[FireDangerDay]] = None
