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
@app_views.route('/states/', methods=['GET'])
def get_states():
    '''get object states'''
    states_get = [data.to_dict() for data in storage.all("State").values()]
    return jsonify(states_get)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    '''individual data-state'''
    states = storage.all("State").values()
    id_state = [data.to_dict() for data in states if data.id == state_id]
    if id_state == []:
        abort(404)
    return jsonify(id_state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def remove_state(state_id):
    '''removes a state'''
    states = storage.all("State").values()
    one_state = [obj.to_dict() for obj in states if obj.id == state_id]
    if one_state == []:
        abort(404)
    one_state.remove(one_state[0])
    matching_states = [data for data in states if data.id == state_id]
    for state in matching_states:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def manufacture_state():
    '''Manufacture or create a new state'''
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    state = State(name=request_data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Updates a State object'''
    states = storage.all(State).values()
    update = next((state for state in states if state.id == state_id), None)
    if update is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    update.name = request.json['name']
    storage.save()
    return jsonify(update.to_dict()), 200
