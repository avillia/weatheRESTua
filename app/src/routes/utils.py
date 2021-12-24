from fastapi import HTTPException

from app.src.extensions.database import session
from app.src.models import Forecast


def check_if_city_exists(city_name: str):
    with session() as db:
        result: list = db.query(Forecast).filter(Forecast.city == city_name).all()
    if not result:
        raise HTTPException(status_code=404, detail="Such city is not found in db!")
