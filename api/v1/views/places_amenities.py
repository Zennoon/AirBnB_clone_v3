#!/usr/bin/python3
"""
Handles RESTful API operations for the relationship between Place
and Amenity objects
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models import storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_amenities_by_place_id(place_id):
    """
    Route function of GET /api/v1/places/<place_id>/amenities

    Retrieves all Amenity objects linked with a Place object
    of given ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == "db":
        return (jsonify([am.to_dict() for am in place.amenities]))
    else:
        amenities = []
        for am_id in place.amenity_ids:
            amenity = storage.get(Amenity, am_id)
            if amenity is not None:
                amenities.append(amenity.to_dict())
        return (jsonify(amenities))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_amenity_from_place(place_id, amenity_id):
    """
    Route function of
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>

    Deletes an Amenity object (or its ID) from a Place object's list of
    amenities
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        idx = place.amenities.index(amenity)
        del place.amenities[idx]
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        idx = place.amenity_ids.index(amenity.id)
        del place.amenity_ids[idx]
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"])
def link_amenity_to_place(place_id, amenity_id):
    """
    Route function of
    POST/api/v1/places/<place_id>/amenities/<amenity_id>

    Links an Amenity object to a Place object
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
