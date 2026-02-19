from fastapi import APIRouter, HTTPException
import yaml

from app.models.weather import WeatherResponse
from app.services.weather import get_weather

router = APIRouter()


def load_locations():
    with open("config.yaml") as f:
        return yaml.safe_load(f)["locations"]


@router.get("/", response_model=list[WeatherResponse])
async def all_locations():
    locations = load_locations()
    results = []
    for loc in locations:
        try:
            results.append(await get_weather(loc["city"], loc["country"]))
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
    return results


@router.get("/{city}", response_model=WeatherResponse)
async def single_location(city: str, country: str = "AU"):
    try:
        return await get_weather(city, country)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
