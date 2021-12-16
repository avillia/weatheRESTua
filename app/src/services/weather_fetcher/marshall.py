from datetime import date

from flask_restful.fields import Float, Integer, MarshallingException, Raw


class Date(Raw):
    def format(self, value):
        try:
            return date.fromtimestamp(value)
        except ValueError as ve:
            raise MarshallingException(ve)


def calculate_mean_temp(temp_dict: dict[str, float]) -> float:
    """
    Need this as far as OpenWeatherMapAPI does not return mean
    temperature by itself, so it's being calculated on our side.
    :param temp_dict:
    :return:
    """
    temp_dict = {
        key: value for key, value in temp_dict.items() if key not in ("max", "min")
    }
    return sum(temp_dict.values()) / len(temp_dict)


forecast_fields = {
    "date": Date(attribute="dt"),
    "temp": Float(attribute=lambda elem: calculate_mean_temp(elem["temp"])),
    "pcp": Float(attribute="rain"),
    "clouds": Integer,
    "pressure": Integer,
    "humidity": Integer,
    "wind_speed": Float,
}
