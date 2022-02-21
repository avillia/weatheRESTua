from app.src.extensions.database import session
from app.src.managers.base import BaseManager
from app.src.models import Forecast


class CityManager(BaseManager):
    model = Forecast

    @classmethod
    def fetch_list_of_cities(cls):
        with session() as db:
            return db.query(cls.model.city).distinct().all()

    @classmethod
    def check_if_city_exists(cls, city_name: str) -> bool:
        with session() as db:
            return bool(db.query(cls.model).filter_by(city=city_name).all())
