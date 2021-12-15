from environs import Env

env = Env()
env.read_env()

FLASK_ENV = env.str("FLASK_ENV", default="development")
PROD_ENV = FLASK_ENV == "production"

SECRET_KEY = env.str("SECRET_KEY", "don't you mind this being a secret key?")

SQLIGHT_DB_FILENAME = env.str("SQLIGHT_DB_FILENAME", "sample_db.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLIGHT_DB_FILENAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", False)

OPENWEATHERMAP_TOKEN = env.str("OPENWEATHERMAP_TOKEN")
