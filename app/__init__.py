from flask import Flask, jsonify, request
from .extensions import api
from mongoengine import connect, Document, StringField

def create_app():
    app = Flask(__name__)
    connect('diddy')
    api.init_app(app)
    return app

class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.objects()
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    user.save()
    return jsonify(user), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects.get(id=user_id)
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.objects.get(id=user_id)
    user.name = data['name']
    user.email = data['email']
    user.save()
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return '', 204
