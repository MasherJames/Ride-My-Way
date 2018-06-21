from flask_restful import Resource, reqparse


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('fullname', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('confirm_password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        request_data = Login.parser.parse_args()

        [fullname, email, password, confirm_password] = request_data


class Signup(Resource):
    def post(self):
        pass
