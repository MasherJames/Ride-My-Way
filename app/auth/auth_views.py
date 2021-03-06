import re
import datetime
from functools import wraps
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity


from ..models import UserRegister


def access_permission(access_id):
    ''' Restrict access levels depending on the permission '''
    def decorator_function(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):
            user = UserRegister().get_by_username(get_jwt_identity())
            if not user.role_level(access_id):
                return {'message': 'Your cannot access this level'}, 401
            return f(*args, **kwargs)
        return wrapper_function

    return decorator_function


class Validation:
    def valid_username(self, username):
        ''' Username should be alphanumeric with atleast 6 characters'''

        return re.match("^[a-zA-Z0-9]{6,}$", username)

    def valid_password(self, password):
        ''' A valid password has atleast one uppercase, one lowercase
    one digit and 6 characters long'''

        return re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{6,}$", password
        )

    def valid_email(self, email):
        ''' Valid email should have an @ symbol and a . after the @ symbol'''

        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_str_fields(self, strings):
        ''' All valid string fields should have alphanumeric characters '''

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

        if not validate.valid_username(username):
            return {
                'message': 'username should be atleast 6 alphanumeric characters'
            }, 400

        if not validate.valid_email(email):
            return {'message': 'Enter a valid email'}, 400

        if not validate.valid_password(password):
            return {
                'message':
                'Password should be atleast 6 characters, a digit,an uppercase and a lowercase'
            }, 400

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
        ''' Login a user it he exists and give him an access token '''

        request_data = Login.parser.parse_args()

        username = request_data['username']

        user_reg = UserRegister()
        user = user_reg.get_by_username(username)

        if user:
            expires = datetime.timedelta(minutes=30)
            token = create_access_token(user.username, expires_delta=expires)
            return {'token': token, 'message': f'You were successfully logged in {username}'}, 200
        return {'message': 'user not found'}, 404
