from datetime import date

from sqlalchemy.orm import load_only

from app.src.extensions.database import session
from app.src.managers.base import BaseManager
from app.src.models import Forecast


class ForecastManager(BaseManager):
    model = Forecast

    @classmethod
    def check_existence_of_forecasts(cls) -> bool:
        with session() as db:
            return bool(db.query(cls.model).all())

    @classmethod
    def obtain_data_for_dataframe(cls, city_name: str, field: str) -> list[Forecast]:
        with session() as db:
            return (
                db.query(cls.model)
                .options(load_only(field))
                .filter_by(city=city_name)
                .all()
            )

    @classmethod
    def obtain_records_for_time_period(
        cls, start_dt: date, end_dt: date, city: str
    ) -> list[Forecast]:
        with session() as db:
            return (
                db.query(cls.model)
                .filter(cls.model.city == city)
                .filter(cls.model.date.between(start_dt, end_dt))
                .all()
            )
