"""Weird stuff goes brrrrrrrrrrrr
This module is created for testing purposes and should run as is.
It creates testing client in main() and then passes it to each 'test',
where the required requests are done."""
from functools import wraps
from json import dumps as json_dump
from typing import Callable

from flask import Flask

from run import app


def print_name_and_args(function: Callable):
    """
    Decorator for pretty-printing the 'test' function, arguments it being
    called with, and the result, which in this case is api response.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"{function.__name__:=^80}")
        print(
            f"Arguments: {args[1:]}\n"
        )  # skip first argument because it is FlaskClient
        print(json_dump(function(*args, **kwargs), indent=4))

    return wrapper


@print_name_and_args
def test_cities(test_env: Flask):
    result = test_env.get("/cities")
    return result.json


@print_name_and_args
def test_mean(test_env: Flask, value_type: str, city: str):
    result = test_env.get(
        "/mean", query_string={"value_type": value_type, "city": city}
    )
    return result.json


@print_name_and_args
def test_records(test_env: Flask, start: str, end: str, city: str):
    result = test_env.get(
        "/records", query_string={"start_dt": start, "end_dt": end, "city": city}
    )
    return result.json


@print_name_and_args
def test_moving_mean(test_env: Flask, value_type: str, city: str):
    result = test_env.get(
        "/moving_mean", query_string={"value_type": value_type, "city": city}
    )
    return result.json


def main():
    with app.test_client() as test_client:
        test_cities(test_client)
        test_mean(test_client, "pcp", "Dnipro")
        test_mean(test_client, "temp", "Kyiv")
        test_mean(test_client, "clouds", "Kryvyj Rih")
        test_records(test_client, "12-07-2000", "21-12-2021", "Kharkiv")
        test_records(test_client, "2000-07-12", "2021-12-21", "Kharkiv")
        test_records(test_client, "2021-12-18", "2021-12-20", "Kharkiv")
        test_moving_mean(test_client, "pressure", "Lviv")
        test_moving_mean(test_client, "clouds", "Odesa")


if __name__ == "__main__":
    main()
