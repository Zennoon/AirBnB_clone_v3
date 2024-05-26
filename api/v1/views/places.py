#!/usr/bin/python3
"""
Handles RESTful API actions for Place class instances
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("cities/<city_id>/places", methods=["GET"])
def get_places_by_city_id(city_id):
    """
    Route function of GET /api/v1/cities/<city_id>/places

    Retrieves all Place objects registered under a City object of given ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return (jsonify(places))


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place_by_id(place_id):
    """
    Route function of GET /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place_by_id(place_id):
    """
    Route function of DELETE /api/v1/places/<place_id>

    Deletes a Place object with given ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """
    Route function of POST /api/v1/cities/<city_id>/places

    Creates a Place object with attributes fromm request body
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    if dct.get("user_id") is None:
        return ("Missing user_id", 400)
    user = storage.get(User, dct.get("user_id"))
    if user is None:
        abort(404)
    if dct.get("name") is None:
        return ("Missing name", 400)
    new_place = Place(city_id=city_id, **dct)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place_by_id(place_id):
    """
    Route function of PUT /api/v1/places/<place_id>

    Modifies a Place object with the given ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, dct[key])
    storage.save()
    return (jsonify(place.to_dict()), 200)
