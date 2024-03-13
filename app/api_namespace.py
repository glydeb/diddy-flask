from flask_restx import Namespace, Resource, fields
from .models import User
from .extensions import db
from .serializers import user_model, user_input_model, user_update_model, authenticate_model
from werkzeug.exceptions import NotFound, Unauthorized
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace('api', description='Diddy API', authorizations=authorizations)

@ns.errorhandler(NotFound)
def handle_no_result_exception(error):
    return {'message': 'User not found'}, 404
@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    @ns.doc(security="jsonWebToken")
    @jwt_required()
    def get(self):
        if current_user.admin:
            return User.query.all(), 200
        else: 
            return User.query.filter_by(id=current_user.id).all(), 200

    @ns.expect(user_input_model)
    @ns.marshal_with(user_model)
    def post(self):
        hashed_password = generate_password_hash(ns.payload['password'])
        user = User(name=ns.payload['name'], email=ns.payload['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route('/users/<user_id>')
@ns.doc(security="jsonWebToken")
class SingleUser(Resource):
    # protect all routes in this class with jwt_required
    method_decorators = [jwt_required()]

    @ns.marshal_with(user_model)
    def get(self, user_id):
        user = db.get_or_404(User, user_id)
        if user:
            return user, 200
        else:
            raise NotFound

    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        user = db.get_or_404(User, user_id)
        user.name = ns.payload['name']
        user.email = ns.payload['email']
        db.session.commit()
        return user, 200

    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

@ns.route('/authenticate')
class Authenticate(Resource):
    @ns.expect(authenticate_model)
    def post(self):
        data = request.json
        query = db.select(User).where(User.email == data['email'])
        user = db.session.execute(query).scalar() # scalar retruns the first result or None
        if not user or not check_password_hash(user.password, data['password']):
            raise Unauthorized('Invalid username or password')
        
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200