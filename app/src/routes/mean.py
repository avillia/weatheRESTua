from enum import Enum
from typing import Optional

from fastapi import APIRouter
from numpy import nan
from pandas import DataFrame
from pydantic import BaseModel
from sqlalchemy.orm import load_only

from app.src.extensions.database import session
from app.src.models import Forecast
from app.src.routes.utils import check_if_city_exists


def form_required_dataframe(city_name: str, field: str) -> DataFrame:
    check_if_city_exists(city_name)
    with session() as db:
        result: list[Forecast] = (
            db.query(Forecast).options(load_only(field)).filter_by(city=city_name).all()
        )
    return DataFrame(elem.as_dataframe_row(field) for elem in result)


def calculate_mean(dataframe: DataFrame, rolling: bool = False, window: int = 2):
    if not rolling:
        return dataframe.mean().replace({nan: None})
    mean: DataFrame = dataframe.rolling(window=window).mean().replace({nan: None})
    return list(zip(*mean.values))[0]


means = APIRouter()


class ValueType(str, Enum):
    temp = "temp"
    pcp = "pcp"
    clouds = "clouds"
    pressure = "pressure"
    humidity = "humidity"
    wind_speed = "wind_speed"


class BaseMean(BaseModel):
    city: str
    value_type: ValueType


class Mean(BaseMean):
    mean: float


class MovingMean(BaseMean):
    window: int
    mean: list[Optional[float]]


@means.get("/mean", tags=["mean"], response_model=Mean)
def mean_value_of_param_for_city(city: str, value_type: ValueType):
    dataframe = form_required_dataframe(city, value_type)
    mean = calculate_mean(dataframe)
    return city, value_type, mean


@means.get("/moving_mean", tags=["mean", "moving mean"], response_model=MovingMean)
def moving_mean_value_of_param_for_city(
    city: str, value_type: ValueType, window: int = 2
):
    dataframe = form_required_dataframe(city, value_type)
    moving_mean = calculate_mean(dataframe, rolling=True, window=window)
    return city, value_type, window, moving_mean
