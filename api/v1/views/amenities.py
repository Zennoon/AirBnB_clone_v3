#!/usr/bin/python3
"""
Handels all default RESTFul API
actions for Amenity objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenities = storage.all(Amenity)
    return (jsonify([amenity.to_dict() for amenity in all_amenities.values()]))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """
    Retrieves a single amenity object by it's id
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return (jsonify(amenity_obj.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """
    Route function of DELETE /api/v1/amenities/<amenity_id>

    Deletes  amenity instance with given ID if it exists
    """
    am_obj = storage.get(Amenity, amenity_id)
    if not am_obj:
        abort(404)
    am_obj.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Route function of POST /api/v1/amenities

    Creates a new Amenity instance with attributes from request body
    """
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    name = dct.get('name')
    if name is None:
        return ('Missing name', 400)
    new_amenity = Amenity(**dct)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """
    Route function for PUT /api/v1/amenities

    Updates Amenity instance with given ID, if it exists
    """
    am_obj = storage.get(Amenity, amenity_id)
    if am_obj is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(am_obj, key, dct[key])
    storage.save()
    return (jsonify(am_obj.to_dict()), 200)
