from fastapi import APIRouter, HTTPException
import yaml

from app.models.weather import WeatherResponse
from app.services.fire import fetch_fire_data
from app.services.weather import get_weather

router = APIRouter()


def load_locations():
    with open("config.yaml") as f:
        return yaml.safe_load(f)["locations"]


@router.get("/", response_model=list[WeatherResponse])
async def all_locations():
    locations = load_locations()
    fire_data = fetch_fire_data()
    results = []
    for loc in locations:
        try:
            results.append(await get_weather(
                loc["city"],
                loc["country"],
                loc["bom_url"],
                fire_district=loc.get("fire_district"),
                show_fire_danger=loc.get("show_fire_danger", False),
                fire_data=fire_data,
                latitude=loc.get("latitude"),
                longitude=loc.get("longitude"),
                location_name=loc.get("name"),
            ))
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
    return results


@router.get("/{city}", response_model=WeatherResponse)
async def single_location(city: str, country: str = "AU", bom_url: str = ""):
    try:
        return await get_weather(city, country, bom_url)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
