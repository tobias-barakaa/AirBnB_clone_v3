#!/usr/bin/python3
""" View for City objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from flasgger.utils import swag_from
from models.city import City
from models import storage_engine


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/cities.yml', methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id: The ID of the State.

    Returns:
        A JSON list of City objects.
    """

    state = storage_engine.get(State, state_id)

    if not state:
        abort(404)

    cities = storage_engine.all(City, state_id=state_id)

    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a City object.

    Args:
        city_id: The ID of the City.

    Returns:
        A JSON object representing the City.
    """

    city = storage_engine.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object.

    Args:
        city_id: The ID of the City.

    Returns:
        An empty dictionary with the status code 200.
    """

    city = storage_engine.get(City, city_id)

    if not city:
        abort(404)

    storage_engine.delete(city)
    storage_engine.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """
    Creates a City object.

    Args:
        state_id: The ID of the State.

    Returns:
        The new City object with the status code 201.
    """

    state = storage_engine.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()

    instance = City(**data)

    instance.state_id = state_id

    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """
    Updates a City object.

    Args:
        city_id: The ID of the City.

    Returns:
        The updated City object with the status code 200.
    """

    city = storage_engine.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    storage_engine.save()

    return make_response(jsonify)
