from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app import ForecastManager
from app.src.routes.utils import throw_error_if_no_such_city_in_db

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
    throw_error_if_no_such_city_in_db(city)
    result = ForecastManager.obtain_records_for_time_period(start_dt, end_dt, city)
    return Records(
        city=city,
        start_dt=start_dt,
        end_dt=end_dt,
        covered_days=len(result),
        values=result,
    )
