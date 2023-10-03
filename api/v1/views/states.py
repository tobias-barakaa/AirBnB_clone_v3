#!/usr/bin/python3
"""
A new view for State objects that handles all default RESTFul API actions.
"""

# Import necessary modules and libraries
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State

# Define a route to retrieve a list of all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON response containing a list of State objects in dictionary format.
    """
    d_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in d_states.values()])

# Define a route to retrieve a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def r_state_id(state_id):
    """
    Retrieves a State object by its ID.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        JSON response containing the State object in dictionary format.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

# Define a route to delete a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """
    Deletes a State object by its ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        Empty JSON response with HTTP status code 200 upon successful deletion.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)

# Define a route to create a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a new State object.

    Returns:
        JSON response containing the newly created State object in dictionary format
        with HTTP status code 201 upon successful creation.
    """
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

# Define a route to update an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates an existing State object by its ID.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        JSON response containing the updated State object in dictionary format
        with HTTP status code 200 upon successful update.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
