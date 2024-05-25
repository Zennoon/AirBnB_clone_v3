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
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
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
    return (jsonify({"error": "Not found"}))


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"),
            threaded=True)
