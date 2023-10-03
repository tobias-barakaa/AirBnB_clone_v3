#!/usr/bin/python3
"""users routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def users_list():
    '''gets list'''
    lists = [data.to_dict() for data in storage.all("User").values()]
    return jsonify(lists)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''gets'''
    users = storage.all("User").values()
    data_user = [data.to_dict() for data in users if data.id == user_id]
    if data_user == []:
        abort(404)
    return jsonify(data_user[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove(user_id):
    '''removes users'''
    users = storage.all("User").values()
    user_data = [data.to_dict() for data in users if data.id == user_id]
    if user_data == []:
        abort(404)
    user_data.remove(user_data[0])
    for obj in users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def manufacture_user():
    '''manufacture a User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    new = User(email=request.json['email'],
               password=request.json['password'])
    storage.new(new)
    storage.save()
    users.append(new.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates(user_id):
    '''Updates'''
    users = storage.all("User").values()
    user_data = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_data == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_data[0]['first_name'] = request.json['first_name']
    except ValueError:
        pass
    try:
        user_data[0]['last_name'] = request.json['last_name']
    except ValueError:
        pass
    for obj in users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except ValueError:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except ValueError:
                pass
    storage.save()
    return jsonify(user_data[0]), 200
