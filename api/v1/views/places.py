#!/usr/bin/python3
"""
Handles RESTful API actions for Place class instances
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models import storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
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


@app_views.route("/places_search", methods=["POST"])
def get_places_by_search_params():
    """
    Route function of POST /api/v1/places_search

    Retrieves Place objects depending on values in the JSON in the
    body of the request

    The JSON is expected to have one
    """
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    filtered_places = []
    state_ids = dct.get("states")
    city_ids = dct.get("cities")
    amenity_ids = dct.get("amenities")

    all_city_ids = set()
    if state_ids is not None:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    all_city_ids.add(city.id)
    if city_ids is not None:
        for city_id in city_ids:
            all_city_ids.add(city_id)

    if all_city_ids:
        for city_id in all_city_ids:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    filtered_places.append(place)
    else:
        filtered_places = list(storage.all(Place).values())
    if amenity_ids is not None:
        if storage_t == "db":
            for amenity_id in amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity is None:
                    continue
                filtered_places = list(
                    filter(
                        lambda place: amenity in place.amenities,
                        filtered_places
                    )
                )

        else:
            for amenity_id in amenity_ids:
                filtered_places = list(
                    filter(
                        lambda place: amenity_id in place.amenity_ids,
                        filtered_places
                    )
                )
    output = []
    for place in filtered_places:
        dct = place.to_dict()
        if dct.get("amenities") is not None:
            del dct["amenities"]
        output.append(dct)

    return (jsonify(output), 200)
