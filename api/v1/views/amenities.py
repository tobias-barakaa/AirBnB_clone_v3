#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/', methods=['GET'])
def lists():
    '''gets and lists the amenities'''
    amenities = [data.to_dict() for data in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''gets amenities'''
    fetch_amenities = storage.all("Amenity").values()
    amenity_data = [data.to_dict() for data in fetch_amenities
                    if data.id == amenity_id]
    if amenity_data == []:
        abort(404)
    return jsonify(amenity_data[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def remove_amenity(amenity_id):
    '''Deletes an Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity_data = [data.to_dict() for data in amenities
                    if data.id == amenity_id]
    if amenity_data == []:
        abort(404)
    amenity_data.remove(amenity_data[0])
    for data in amenities:
        if data.id == amenity_id:
            storage.delete(data)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def manufacture_amenity():
    '''manufaacture amenities'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new = Amenity(name=request.json['name'])
    storage.new(new)
    storage.save()
    amenities.append(new.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates an Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity_data = [data.to_dict() for data in amenities
                    if data.id == amenity_id]
    if amenity_data == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_data[0]['name'] = request.json['name']
    for data in amenities:
        if data.id == amenity_id:
            data.name = request.json['name']
    storage.save()
    return jsonify(amenity_data[0]), 200
