from datetime import date
from typing import List, Optional, Union

import requests
from pydantic import BaseModel

from app.configs import OPENWEATHERMAP_TOKEN


class Forecast(BaseModel):
    date: date
    temp: float
    pcp: Optional[float]
    clouds: int
    pressure: int
    humidity: int
    wind_speed: float


def calculate_mean_temp(temp_dict: dict[str, float]) -> float:
    """
    Need this as far as OpenWeatherMapAPI does not return mean
    temperature by itself, so it's being calculated on our side.
    :param temp_dict:
    :return:
    """
    temp_dict = {
        key: value for key, value in temp_dict.items() if key not in ("max", "min")
    }
    return sum(temp_dict.values()) / len(temp_dict)


def obtain_weather_for_city(city_name: str) -> list[Forecast]:
    """
    For some reason they are not letting you retrieve weather for
    7 days via city name in free tier, but they left an opportunity
    to fetch longitude and latitude by name. So I'm fetching lat and lon,
    and then retrieve weather for them.
    :param city_name:
    :return: list of 7 marshalled dicts that include weather forecasts
    """
    city_data = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct",
        params={"q": city_name, "limit": 1, "appid": OPENWEATHERMAP_TOKEN},
    ).json()
    latitude, longitude = city_data[0]["lat"], city_data[0]["lon"]
    data = requests.get(
        "https://api.openweathermap.org/data/2.5/onecall",
        params={
            "lat": latitude,
            "lon": longitude,
            "exclude": "current,minutely,hourly,alerts",
            "appid": OPENWEATHERMAP_TOKEN,
        },
    ).json()

    return [
        Forecast(
            date=day.get("dt"),
            temp=calculate_mean_temp(day.get("temp")),
            pcp=day.get("rain"),
            clouds=day.get("clouds"),
            pressure=day.get("pressure"),
            humidity=day.get("humidity"),
            wind_speed=day.get("wind_speed"),
        )
        for day in data.get("daily")
    ]


def obtain_weather_for_5_cities(
    cities: Optional[list[str]] = None,
) -> list[dict[str, Union[int, float, str, None]]]:
    if cities is None:
        cities = ["Dnipro", "Lviv", "Kyiv", "Odesa", "Kharkiv"]

    forecasts_to_add = []
    for city in cities:
        for day in obtain_weather_for_city(city):
            fields: dict[str, Union[int, float, str, None]]  # just for lovely mypy
            fields = {"city": city, **day.dict()}
            forecasts_to_add.append(fields)

    return forecasts_to_add
