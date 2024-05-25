from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """Route function for /api/v1/status"""
    return (jsonify({"status": "OK"}))
