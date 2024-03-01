from flask_restx import Namespace, Resource
from .models import User
from .extensions import db
from .serializers import user_model, user_input_model
from werkzeug.exceptions import NotFound, BadRequest

ns = Namespace('api', description='Diddy API')

@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @ns.expect(user_input_model)
    @ns.marshal_with(user_model)
    def post(self):
        user = User(name=ns.payload['name'], email=ns.payload['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route('/users/<user_id>')
class SingleUser(Resource):
    @ns.marshal_list_with(user_model)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user, 200
        else:
            raise NotFound(f"User with id {user_id} not found")

#     def put(self, user_id):
#         data = request.get_json()
#         user = User.objects.get(id=user_id)
#         user.name = data['name']
#         user.email = data['email']
#         user.save()
#         return jsonify(user), 200

#     def delete(self, user_id):
#         user = User.objects.get(id=user_id)
#         user.delete()
#         return '', 204

# @ns.route('/users', methods=['GET'])
# def get_users():
#     users = User.objects()
#     return jsonify(users), 200

# @ns.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     user = User(name=data['name'], email=data['email'])
#     user.save()
#     return jsonify(user), 201

# @ns.route('/users/<user_id>', methods=['GET'])
# def get_user(user_id):
#     user = User.objects.get(id=user_id)
#     return jsonify(user), 200

# @ns.route('/users/<user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.get_json()
#     user = User.objects.get(id=user_id)
#     user.name = data['name']
#     user.email = data['email']
#     user.save()
#     return jsonify(user), 200

# @ns.route('/users/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.objects.get(id=user_id)
#     user.delete()
#     return '', 204