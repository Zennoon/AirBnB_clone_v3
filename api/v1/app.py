#!/usr/bin/python3
"""
Contains:
    Misc
    ====
    Script to initialize a flask application
"""
import os
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": "0.0.0.0"}
})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def renew_session(exc):
    """
    Renews the storage session after every request to
    reflect any changes made
    """
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """
    Error handler for non-found resources
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"),
            threaded=True)
