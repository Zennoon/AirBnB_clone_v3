#!/usr/bin/python3
"""
Handles REST API operations for Review objects
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews_by_place_id(place_id):
    """
    Route function of GET /api/v1/places/<place_id>/reviews

    Retrieves all Review objects registered with the given place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return (jsonify(reviews))


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_by_id(review_id):
    """
    Route function of GET /api/v1/reviews/<review_id>

    Retrieves a Review object with the given id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review_by_id(review_id):
    """
    Route function of DELETE /api/v1/reviews/<review_id>

    Deletes a Review object with the given ID if it exists
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """
    Route function for POST /api/v1/places/<place_id>/reviews

    Creates a new Review object with attribute values from request body
    """
    place = storage.get(Place, place_id)
    if place is None:
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
    if dct.get("text") is None:
        return ("Missing text", 400)
    new_review = Review(place_id=place_id, **dct)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review_by_id(review_id):
    """
    Route function of PUT /api/v1/reviews/<review_id>

    Modifies a Review object with given ID with attributes from the
    request body
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    try:
        dct = request.get_json()
    except Exception:
        return ("Not a JSON", 400)
    for key in dct.keys():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, dct[key])
    storage.save()
    return (jsonify(review.to_dict()), 200)
