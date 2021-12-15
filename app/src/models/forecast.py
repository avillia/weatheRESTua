from sqlalchemy import Column, Date, Float, Integer, String

from app.src.extensions.database import Base


class PandasModelMixin:
    def as_dataframe_row(self, *args: str):
        dict_repr = self.__dict__.items()
        if args:
            return {key: value for key, value in dict_repr if key in args}
        return {
            key: value for key, value in dict_repr if key not in ("_sa_instance_state",)
        }


class Forecast(Base, PandasModelMixin):
    __tablename__ = "forecasts"

    date = Column(Date, primary_key=True)
    city = Column(String, primary_key=True)

    temp = Column(Float)
    pcp = Column(Float)
    clouds = Column(Integer)
    pressure = Column(Integer)
    humidity = Column(Integer)
    wind_speed = Column(Float)
