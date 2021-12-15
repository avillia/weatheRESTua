from flask_restful import Resource, marshal_with
from flask_restful.fields import Float, Integer, List, String
from flask_restful.reqparse import RequestParser

from app.src.handlers.mean import (  # isort:skip
    calculate_mean_value_for_city,  # isort:skip
    calculate_rolling_mean_value_for_city,  # isort:skip
)  # isort:skip

mean_response_fields = {"city": String, "value_type": String, "mean": Float}

moving_mean_response_fields = {
    "city": String,
    "value_type": String,
    "window": Integer,
    "moving_mean": List(Float),
}

get_mean_parser = RequestParser()
get_mean_parser.add_argument(
    "value_type",
    dest="field",
    required=True,
    choices=["temp", "pcp", "clouds", "pressure", "humidity", "wind_speed"],
)
get_mean_parser.add_argument("city", dest="city_name", required=True)


class MeanParam(Resource):
    @marshal_with(mean_response_fields)
    def get(self):  # pylint: disable=no-self-use
        args = get_mean_parser.parse_args()
        return calculate_mean_value_for_city(**args)


class MovingMeanParam(Resource):
    @marshal_with(moving_mean_response_fields)
    def get(self):  # pylint: disable=no-self-use
        args = get_mean_parser.parse_args()
        return calculate_rolling_mean_value_for_city(**args)
