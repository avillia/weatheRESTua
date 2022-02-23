from fastapi import APIRouter
from pydantic import BaseModel

from app.src.managers import SQLAlchemyCityManager as CityManager


class Cities(BaseModel):
    cities: list[str]


cities = APIRouter()


@cities.get("/cities", tags=["cities"], response_model=Cities)
def obtain_list_of_cities():
    result = CityManager.fetch_list_of_cities()
    return Cities(cities=[forecast.city for forecast in result])
