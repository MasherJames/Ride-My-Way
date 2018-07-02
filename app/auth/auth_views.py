from flask import request
import re
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)

from ..models import UserRegister


class Validation:

    def valid_username(self, username):
        return re.match("^[a-zA-Z0-9]{6,}$", username)

    def valid_password(self, password):
        return re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{6,}$", password)

    def valid_email(self, email):
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_str_fields(self, strings):
        return re.match("^[a-zA-Z0-9-\._@]+$", strings)


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

    def post(self):
        request_data = Signup.parser.parse_args()

        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        permission = request_data['permission']

        validate = Validation()
        user_reg = UserRegister()

        if not validate.valid_username(request_data['username']):
            return {'message': 'username should be atleast 6 character and valid'}, 400

        if not validate.valid_email(request_data['email']):
            return {'message': 'Enter a valid email'}, 400

        if not validate.valid_password(request_data['password']):
            return {'message': 'Password should be atleast 6 characters, a digit, an uppercase and a lowercase'}, 400

        if user_reg.get_by_username(username):
            return {'message': 'user with the username {} already exists'
                    .format(username)}, 400

        if user_reg.get_by_email(email):
            return {'message': 'This email is already in use'}, 400

        user = UserRegister(username, email, password, permission)
        user.add()
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

        user_reg = UserRegister()
        user = user_reg.get_by_username(username)

        if user:
            token = create_access_token(user.username)
            return {'token': token}, 200
        return {'message': 'user not found'}, 404
