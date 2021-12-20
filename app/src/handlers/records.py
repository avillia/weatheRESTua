from datetime import date
from typing import Union

from app.src.extensions.database import session
from app.src.handlers.utils import check_if_city_exists
from app.src.models import Forecast


def fetch_records_for_time_period(
    city_name: str, start: date, end: date
) -> dict[str, Union[str, date, int, list[Forecast]]]:
    check_if_city_exists(city_name)
    with session() as db:
        result: list[Forecast] = (
            db.query(Forecast)
            .filter(Forecast.city == city_name, Forecast.date.between(start, end))
            .all()
        )
    return {
        "city": city_name,
        "start_dt": start,
        "end_dt": end,
        "covered_days": len(result),
        "values": result,
    }
