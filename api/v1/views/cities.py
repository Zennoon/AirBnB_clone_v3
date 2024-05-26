#!/usr/bin/python3
"""
Handels all default RESTFul API
actions for Amenity objects
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state_id(state_id):
    """
    Route function for GET /api/v1/states/<state_id>/cities

    Retrieves all City objects registered with a State of given ID
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return (jsonify(cities))


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_by_id(city_id):
    """
    Route function for GET /api/v1/cities/<city_id>

    Retrieves a City instance with the given ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city_by_id(city_id):
    """
    Route function of DELETE /api/v1/cities/<city_id>

    Retrieves a City object with the given ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Route function of POST /api/v1/<state_id>/cities

    Create a new City instance with the given State ID and attributes
    from the request body
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    name = dct.get("name")
    if name is None:
        return ("Missing name", 400)
    new_city = City(state_id=state_id, **dct)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city_by_id(city_id):
    """
    Route function of PUT /api/v1/cities/<city_id>

    Modifies a City instance with the given ID using attributes
    in the request body
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, dct[key])
    storage.save()
    return (jsonify(city.to_dict()), 200)
