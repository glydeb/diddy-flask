from flask_restx import fields

from .extensions import api

user_model = api.model('User', {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
})

user_input_model = api.model('User', {
    "name": fields.String,
    "email": fields.String
})