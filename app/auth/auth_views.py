from flask import request
from flask_restful import Resource, reqparse
from ..models import User, store


class Signup(Resource):

    @classmethod
    def find_user_by_email(cls, email):
        return [user['email'] for user in store['users']] == email

    def post(self):
        request_data = request.get_json()
        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        permission = request_data['username']

        if Signup.find_user_by_email(email):
            return {'message': 'user with the email {} already exists'
                    .format(email)}, 400

        user = User(username, email, password, permission)
        store['users'].append(user)
        return user


# class Login(Resource):

#     def post(self):
#         request_data = Login.parser.parse_args()

#         [fullname, email, password, confirm_password] = request_data
