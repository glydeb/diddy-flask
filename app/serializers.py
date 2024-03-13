from flask_restx import fields

from .extensions import api

user_model = api.model('User', {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
})

user_input_model = api.model('User', {
    "name": fields.String,
    "email": fields.String,
    "password": fields.String
})

user_update_model = api.model('User', {
    "name": fields.String,
    "email": fields.String,
    "admin": fields.Boolean # only admin can change this field
})

authenticate_model = api.model('UserInput', {
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='Password')
})
