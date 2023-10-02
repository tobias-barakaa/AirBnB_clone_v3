#!/usr/bin/python3
"""
running first ap
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

classes = [Amenity, City, Place, Review, State, User]
names = ["amenities", "cities", "places", "reviews", "states", "users"]


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    This function defines a route that returns a
    JSON response with the status "OK".

    Returns:
        JSON response with the status "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the number of each object.
    """
    list = {}
    for k in range(len(classes)):
        list[names[k]] = storage.count(classes[k])

    return jsonify(list)
