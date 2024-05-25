from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity, 
    "cities": City, 
    "places": Place, 
    "reviews": Review, 
    "states": State, 
    "users": User
}

@app_views.route("/status")
def status():
    """Route function for /api/v1/status"""
    return (jsonify({"status": "OK"}))

@app_views.route("/stats")
def stats():
    """
    Route function for /api/v1/stats
    
    Displays the number of objects of each class
    """
    objs = {}
    for cls in classes.keys():
        objs[key] = storage.count(classes[cls])
    return (jsonify(objs))
