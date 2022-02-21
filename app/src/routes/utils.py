from fastapi import HTTPException

from app.src.managers import CityManager


def throw_error_if_no_such_city_in_db(city_name: str):
    if not CityManager.check_if_city_exists(city_name):
        raise HTTPException(status_code=404, detail="Such city is not found in db!")
