from datetime import date, datetime

from flask_restful import Resource, marshal_with
from flask_restful.fields import Float, Integer, List, Nested, String
from flask_restful.reqparse import RequestParser

from app.src.handlers.records import fetch_records_for_time_period

mean_response_fields = {
    "city": String,
    "start_dt": String,
    "end_dt": String,
    "covered_days": Integer,
    "values": List(
        Nested(
            {
                "temp": Float,
                "pcp": Float,
                "clouds": Integer,
                "pressure": Integer,
                "humidity": Integer,
                "wind_speed": Float,
            }
        )
    ),
}


def date_str(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


get_records_parser = RequestParser()
get_records_parser.add_argument("start_dt", dest="start", required=True, type=date_str)
get_records_parser.add_argument("end_dt", dest="end", required=True, type=date_str)
get_records_parser.add_argument("city", dest="city_name", required=True)


class Records(Resource):
    @marshal_with(mean_response_fields)
    def get(self):  # pylint: disable=no-self-use
        args = get_records_parser.parse_args()
        return fetch_records_for_time_period(**args)
