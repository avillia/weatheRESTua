from fastapi import APIRouter

from app.src.extensions.database import session
from app.src.models import Forecast

cities = APIRouter()


@cities.get("/cities", tags=["cities"])
def obtain_list_of_cities():
    with session() as db:
        result: list[Forecast] = db.query(Forecast.city).distinct().all()
    return {"cities": [forecast.city for forecast in result]}
