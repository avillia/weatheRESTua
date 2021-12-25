from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.src.extensions.database import session
from app.src.models import Forecast


class Cities(BaseModel):
    cities: list[str]


cities = APIRouter()


@cities.get("/cities", tags=["cities"], response_model=Cities)
def obtain_list_of_cities():
    with session() as db:
        result: list[Forecast] = db.query(Forecast.city).distinct().all()
    return [forecast.city for forecast in result]
