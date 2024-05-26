#!/usr/bin/python3
"""
Contains:
    RESTful API action handler functions for the State class
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_all_users():
    """
    Route function of GET /api/v1/users

    Retrieves all User instances in storage
    """
    all_users = storage.all(User)
    return (jsonify([user.to_dict() for user in all_users.values()]))


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Route function of GET /api/v1/users/<user_id>

    Retrieves a single User instance with the given ID
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    """
    Route function of DELETE /api/v1/users/<user_id>

    Deletes a User instance with given ID from storage
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    """
    Route function of POST /api/v1/users

    Creates a new User instance with instance values from request body
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
def update_user_by_id(user_id):
    """
    Route function of PUT /api/v1/users/<user_id>

    Modifies a User instance with the given ID using attributes
    given by the request body
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, dct[key])
    storage.save()
    return (jsonify(user.to_dict()), 200)
