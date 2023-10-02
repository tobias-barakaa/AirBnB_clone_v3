#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@states_bp.route('/', methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@states_bp.route('/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@states_bp.route('/', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@states_bp.route('/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())

@states_bp.route('/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})
