#!/usr/bin/python3
"""
running first app
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    """
    This function defines a route that returns a JSON response with the status "OK".

    Returns:
        JSON response with the status "OK"
    """
    return {"status": "OK"}, 200
