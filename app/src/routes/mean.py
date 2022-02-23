from enum import Enum
from typing import Optional

from fastapi import APIRouter
from numpy import nan
from pandas import DataFrame
from pydantic import BaseModel

from app.src.managers import SQLAlchemyForecastManager as ForecastManager
from app.src.routes.utils import throw_error_if_no_such_city_in_db


def form_required_dataframe(city_name: str, field: str) -> DataFrame:
    result = ForecastManager.obtain_data_for_dataframe(city_name, field)
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
    throw_error_if_no_such_city_in_db(city)
    dataframe = form_required_dataframe(city, value_type)
    mean = calculate_mean(dataframe)
    return Mean(city=city, value_type=value_type, mean=mean)


@means.get("/moving_mean", tags=["mean", "moving mean"], response_model=MovingMean)
def moving_mean_value_of_param_for_city(
    city: str, value_type: ValueType, window: int = 2
):
    throw_error_if_no_such_city_in_db(city)
    dataframe = form_required_dataframe(city, value_type)
    moving_mean = calculate_mean(dataframe, rolling=True, window=window)
    return MovingMean(
        city=city, value_type=value_type, window=window, moving_mean=moving_mean
    )
