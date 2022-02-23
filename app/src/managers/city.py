from typing import Any

from app.src.extensions.database import session
from app.src.managers.base import SQLAlchemyBaseManager
from app.src.models import Forecast


class BaseCityManager:
    """Interface for CityManagers. Only to be inherited from."""

    @classmethod
    def fetch_list_of_cities(cls) -> Any:
        return NotImplemented

    @classmethod
    def check_if_city_exists(cls, city_name: str) -> bool:
        raise NotImplemented


class SQLAlchemyCityManager(SQLAlchemyBaseManager, BaseCityManager):
    model = Forecast

    @classmethod
    def fetch_list_of_cities(cls) -> list[Forecast]:
        with session() as db:
            return db.query(cls.model.city).distinct().all()

    @classmethod
    def check_if_city_exists(cls, city_name: str) -> bool:
        with session() as db:
            return bool(db.query(cls.model).filter_by(city=city_name).all())
