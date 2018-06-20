from datetime import datetime
from app import app
import unittest
import json


class TestRideOffers(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.data = {
            "signup-cred": {
                "fullname": "james mash",
                "email": "jamesmash@gmail.com",
                "password": "qwerty",
                "confirm-password": "qwerty"
            },
            "login-cred": {
                "email": "jamesmash@gmail.com",
                "password": "qwerty"
            }
        }

    def tearDown(self):
        pass

    '''
    sign up function
    '''

    def signup(self):
        response = self.client.post(
            "/api/v1/auth/signup/",
            data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )
        return response

    '''
    login function
    '''

    def login(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            data=json.dumps(self.data['login-cred']),
            headers={'content-type': 'application/json'})

        return response
    '''
    get token function
    '''

    def get_user_token(self):
        self.signup()
        response = self.login()
        token = json.loads(response.data).get('token')

        return token

    def test_user_get_token(self):
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

        self.assertIn('token', json.loads(response.data))

    def test_user_can_view_all_ride_offers(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides/",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {} '.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_a_specific_ride_offer(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides/<rideId >/",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {} '.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_ride_offer(self):
        token = self.get_user_token()

        data = {
            "driver's name": "joseph",
            "from": "Nakuru",
            "to": "ruiru",
            "datetime": str(datetime.now())
        }
        response = self.client.post(
            "/api/v1/rides/", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {} '.format(token)}
        )

        self.assertEqual(response.status_code, 201)

    def test_user_can_request_a_ride(self):
        token = self.get_user_token()

        data = {
            "name": "james mas",
            "datetime": str(datetime.now()),
            "from": "Rongai",
            "to": "Burubur"
        }

        response = self.client.post(
            "/rides/<rideId >/requests", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {} '.format(token)}
        )
        self.assertEqual(response.status_code, 202)
