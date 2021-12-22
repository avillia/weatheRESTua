from fastapi import FastAPI

from app.src.extensions import database
from app.src.models import Forecast
from app.src.routes import routers
from app.src.services import weather_fetcher


def register_resources(app: FastAPI):
    for router in routers:
        app.include_router(router)

    return app


def init_db():
    database.Base.metadata.create_all(bind=database.engine)


def populate_db_if_empty():
    with database.session() as db:
        if not db.query(Forecast).all():
            for data in weather_fetcher.obtain_weather_for_5_cities():
                db.add(Forecast(**data))
            db.commit()


def create_app():
    app = FastAPI()
    init_db()
    populate_db_if_empty()
    register_resources(app)

    return app
