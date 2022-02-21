from sqlalchemy import Column, Date, Float, Integer, String

from app.src.extensions.database import Base, session
from app.src.models.utils import PandasModelMixin


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
