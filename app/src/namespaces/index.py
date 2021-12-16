from flask_restful import Resource, marshal_with
from flask_restful.fields import List, String


index_fields = {
    "status": String,
    "endpoints": List(String),
    "how_to_use": String,
    "sample_request": String,
}


class Index(Resource):
    @marshal_with(index_fields)
    def get(self):  # pylint: disable=no-self-use
        return {
            "status": "alive",
            "endpoints": [
                "/cities",
                "/mean",
                "/records",
                "/moving_mean",
            ],
            "how_to_use": "Provide your arguments as query parameters!",
            "sample_request": "/records?start_dt=2021-12-17&end_dt=2021-12-18&city=Dnipro",
        }
