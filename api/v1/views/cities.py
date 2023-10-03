#!/usr/bin/python3
"""
New view for City objects that handles all default RESTFul API actions.
"""

from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from api.v1.views import app_views
from api.v1.views.states import get_state


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id (str): The ID of the State
        object to retrieve City objects from.

    Returns:
        JSON response containing a list of City objects in dictionary format.
    """
    state = get_state(state_id)
    if not state:
        abort(404)

    cities = storage.all(City).values()
    stat_ct = [city.to_dict() for city in cities if city.state_id == state_id]
    return jsonify(state_ct)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its ID.

    Args:
        city_id (str): The ID of the City object to retrieve.

    Returns:
        JSON response containing the City object in dictionary format.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its ID.

    Args:
        city_id (str): The ID of the City object to delete.

    Returns:
        Empty JSON response with HTTP status code 200 upon successful deletion.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object within a State.

    Args:
        state_id (str): The ID of the State object to which the City belongs.

    Returns:
        JSON response containing the newly created
        City object in dictionary format
        with HTTP status code 201 upon successful creation.
    """
    state = get_state(state_id)
    if not state:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    request_data['state_id'] = state_id
    city = City(**request_data)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object by its ID.

    Args:
        city_id (str): The ID of the City object to update.

    Returns:
        JSON response containing the updated City object in dictionary format
        with HTTP status code 200 upon successful update.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    # Update the City object with the new data, ignoring specific keys
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
