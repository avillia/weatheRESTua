from typing import Optional, Union

from pandas import DataFrame
from sqlalchemy.orm import load_only

from app.src.extensions.database import session
from app.src.handlers.utils import check_if_city_exists
from app.src.models import Forecast


def form_required_dataframe(city_name: str, field: str) -> DataFrame:
    check_if_city_exists(city_name)
    with session() as db:
        result: list[Forecast] = (
            db.query(Forecast).options(load_only(field)).filter_by(city=city_name).all()
        )
    return DataFrame(elem.as_dataframe_row(field) for elem in result)


def calculate_mean_value_for_city(
    city_name: str, field: str
) -> dict[str, Union[str, float]]:
    dataframe = form_required_dataframe(city_name, field)
    return {"city": city_name, "value_type": field, "mean": dataframe.mean()}


def calculate_rolling_mean_value_for_city(
    city_name: str, field: str, window: int = 2
) -> dict[str, Union[str, int, list[Optional[float]]]]:
    dataframe = form_required_dataframe(city_name, field)
    mean: DataFrame = dataframe.rolling(window=window).mean()
    moving_mean = list(zip(*mean.values))[0]
    return {
        "city": city_name,
        "value_type": field,
        "window": window,
        "moving_mean": moving_mean,
    }
