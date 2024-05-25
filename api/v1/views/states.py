#!/usr/bin/python3
"""
Handles RESTful API actions for the State class
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def get_states():
    """
    Route function of GET /api/v1/states

    Returns all State objects' representations
    """
    all_states = storage.all(State)
    return (jsonify([state.to_dict() for state in all_states.values()]))


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """
    Route function of GET /api/v1/states/<state_id>

    Returns representation of a state of given ID, if it exists
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Route function of DELETE /api/v1/states/<state_id>

    Deletes a State instance with given ID if it exists
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    """
    Route function of POST /api/v1/states

    Creates a new State instance with attributes from request body
    """
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    name = dct.get("name")
    if name is None:
        return ("Missing name", 400)
    new_state = State(**dct)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Route function for PUT /api/v1/states

    Updates a State instance with given ID, if it exists
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, dct[key])
    storage.save()
    return (jsonify(state.to_dict()), 200)
