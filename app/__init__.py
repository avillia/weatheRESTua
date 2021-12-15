from flask import Flask


def create_app(config_object="app.configs"):
    app = Flask("weatheRESTua", static_folder="app/src/static")
    app.config.from_object(config_object)

    return app
