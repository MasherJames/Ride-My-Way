from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)
# from ..models import UserRegister, UserLogin, store


class Signup(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('permission', required=True,
                        help='This field cannot be left blank')

    @classmethod
    def find_user_by_username(cls, username):
        for user in store['users']:
            return user.username == username

    @classmethod
    def get_user_by_username(cls, username, password):
        for user in store['users']:
            if user.username == username and user.check_password(password):
                return user

    def post(self):
        request_data = Signup.parser.parse_args()

        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        permission = request_data['permission']

        if Signup.find_user_by_username(username):
            return {'message': 'user with the username {} already exists'
                    .format(username)}, 400

        user = UserRegister(username, email, password, permission)
        store['users'].append(user)
        return {'message': 'user created successfully'}, 201


class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', required=True,
                        help='This field cannot be left blank')

    def post(self):
        request_data = Login.parser.parse_args()

        username = request_data['username']
        password = request_data['password']

        user = Signup.get_user_by_username(username, password)

        if user:
            token = create_access_token(user.username)
            return {'token': token}, 200
        return {'message': 'user not found'}, 404
