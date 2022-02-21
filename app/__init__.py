from fastapi import FastAPI

from app.src.extensions import database
from app.src.managers import ForecastManager
from app.src.routes import routers
from app.src.services import weather_fetcher


def register_resources(app: FastAPI) -> FastAPI:
    for router in routers:
        app.include_router(router)

    return app


def init_db() -> None:
    database.Base.metadata.create_all(bind=database.engine)


def populate_db_if_empty() -> None:
    if not ForecastManager.check_existence_of_forecasts():
        data = weather_fetcher.obtain_weather_for_5_cities()
        ForecastManager.create_multiple_from_list(data)


def create_app() -> FastAPI:
    app = FastAPI()
    init_db()
    populate_db_if_empty()
    register_resources(app)

    return app
