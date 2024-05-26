#!/usr/bin/python3
"""
Handels all default RESTFul API
actions for User objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=["GET"])
def get_all_users():
    """
    Retrieves all User instances
    """
    all_users = storage.all(User)
    return (jsonify([user.to_dict() for user in all_users.values()]))
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Retrieves a single User object by it's id
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return (jsonify(user_obj.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """
    Route function of DELETE /api/v1/users/<user_id>

    Deletes  User instance with given ID if it exists
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    user_obj.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Route function of POST /api/v1/users

    Creates a new User instance with attributes from request body
    """
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for attr in ["email", "password"]:
        if dct.get(attr) is None:
            return ("Missing {}".format(attr), 400)
    new_user = User(**dct)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Route function for PUT /api/v1/users

    Updates User instance with given ID, if it exists
    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, dct[key])
    storage.save()
    return (jsonify(user_obj.to_dict()), 200)
