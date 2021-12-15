from flask import Flask
from flask_restful import Api

from app.src.extensions import database
from app.src.models import Forecast
from app.src.namespaces import Cities, Mean, MovingMean, Records
from app.src.services import weather_fetcher


def register_resources(app: Flask):
    api = Api()

    api.add_resource(Cities, "/cities")
    api.add_resource(Mean, "/mean")
    api.add_resource(MovingMean, "/moving_mean")
    api.add_resource(Records, "/records")

    api.init_app(app)

    return app


def init_db(app: Flask):
    database.Base.metadata.create_all(bind=database.engine)
    return app


def populate_db_if_empty():
    with database.session() as db:
        if not db.query(Forecast).all():
            for data in weather_fetcher.obtain_weather_for_5_cities():
                db.add(Forecast(**data))
            db.commit()


def create_app(config_object="app.configs"):
    app = Flask("weatheRESTua", static_folder="app/src/static")
    app.config.from_object(config_object)
    init_db(app)
    populate_db_if_empty()
    register_resources(app)

    return app
