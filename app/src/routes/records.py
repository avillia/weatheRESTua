from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.src.extensions.database import session
from app.src.models import Forecast as ForecastORM
from app.src.routes.utils import check_if_city_exists

records = APIRouter()


class Forecast(BaseModel):
    temp: float
    pcp: Optional[float]
    clouds: int
    pressure: int
    humidity: int
    wind_speed: float

    class Config:
        orm_mode = True


class Records(BaseModel):
    city: str
    start_dt: date
    end_dt: date
    covered_days: int
    values: list[Forecast]


@records.get("/records", tags=["cities", "records"], response_model=Records)
def records_for_time_period(start_dt: date, end_dt: date, city: str):
    check_if_city_exists(city)
    with session() as db:
        result: list[ForecastORM] = (
            db.query(ForecastORM)
            .filter(ForecastORM.city == city)
            .filter(ForecastORM.date.between(start_dt, end_dt))
            .all()
        )
    return {
        "city": city,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "covered_days": len(result),
        "values": result,
    }
