from flask_restful import Resource, marshal_with
from flask_restful.fields import List, String

from app.src.handlers.cities import fetch_cities_in_db

cities_list_response = {"cities": List(String(attribute="city"))}


class Cities(Resource):
    @marshal_with(cities_list_response)
    def get(self):  # pylint: disable=no-self-use
        return fetch_cities_in_db()
