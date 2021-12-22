from datetime import date

from fastapi import APIRouter

from app.src.extensions.database import session
from app.src.helpers.utils import check_if_city_exists
from app.src.models import Forecast

records = APIRouter()


@records.get("/records", tags=["cities", "records"])
def records_for_time_period(start_dt: date, end_dt: date, city: str):
    check_if_city_exists(city)
    with session() as db:
        result: list[Forecast] = (
            db.query(
                Forecast.pcp,
                Forecast.temp,
                Forecast.clouds,
                Forecast.humidity,
                Forecast.wind_speed,
                Forecast.pressure,
            )
            .filter(Forecast.city == city)
            .filter(Forecast.date.between(start_dt, end_dt))
            .all()
        )
    return {
        "city": city,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "covered_days": len(result),
        "values": result,
    }
