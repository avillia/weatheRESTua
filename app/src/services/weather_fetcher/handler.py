from typing import Optional, Union

import requests
from flask_restful import marshal

from app.configs import OPENWEATHERMAP_TOKEN
from app.src.services.weather_fetcher.marshall import forecast_fields


def obtain_weather_for_city(city_name: str) -> list[dict[str, Union[int, float]]]:
    """
    For some reason they are not letting you to retrieve weather for
    7 days via city name in free tier, but they left an opportunity
    to fetch longitude and latitude by name. So i'm fetching lat and lon,
    and then retrieve weather for them.
    :param city_name:
    :return: list of 7 marshalled dicts that include weather forecasts
    """
    city_data = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
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

    return [marshal(day, forecast_fields) for day in data["daily"]]


def obtain_weather_for_5_cities(
    cities: Optional[list[str]] = None,
) -> list[dict[str, Union[int, float, str]]]:
    if cities is None:
        cities = ["Dnipro", "Lviv", "Kyiv", "Odesa", "Kharkiv"]
    forecasts_to_add = []
    for city in cities:
        for day in obtain_weather_for_city(city):
            fields: dict[str, Union[int, float, str]] = {"city": city, **day}
            forecasts_to_add.append(fields)
    return forecasts_to_add
