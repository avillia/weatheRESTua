from app.src.extensions.database import session
from app.src.models import Forecast


def fetch_cities_in_db() -> dict[str, list[Forecast]]:
    with session() as db:
        result: list[Forecast] = db.query(Forecast.city).distinct().all()
    return {"cities": result}
