from environs import Env

env = Env()
env.read_env()

SQLALCHEMY_DATABASE_URI = f"sqlite:///{env.str('SQLIGHT_DB_FILENAME', 'sample_db.db')}"

OPENWEATHERMAP_TOKEN = env.str("OPENWEATHERMAP_TOKEN")
