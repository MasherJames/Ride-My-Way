from app import create_app
import unittest
import json


class TestRideOffers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.data = {
            "signup-cred": {
                "username": "macharia",
                "email": "jamesmash@gmail.com",
                "password": "qwerty",
                "permission": 1
            },
            "login-cred": {
                "username": "macharia",
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
            "/api/v1/auth/signup",
            data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )

        return response

    '''
    login function
    '''

    def login(self):
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.data['login-cred']),
            headers={'content-type': 'application/json'}
        )

        return response

    def test_signup(self):
        response = self.signup()

        self.assertEqual(response.status_code, 201)

    def test_login(self):
        ''' signup a user first '''
        self.signup()
        response = self.login()

        self.assertEqual(response.status_code, 200)

    '''
    get token function
    '''

    def get_user_token(self):
        self.signup()
        response = self.login()
        token = json.loads(response.data).get('token', None)

        return token

    def test_user_get_token(self):
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

        self.assertIn('token', json.loads(response.data))

    def test_user_can_view_all_ride_offers(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_a_specific_ride_offer(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides/<rideId>",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_ride_offer(self):
        token = self.get_user_token()

        data = {
            "driver_name": "joseph",
            "from": "Nakuru",
            "to": "ruiru",
            "depature": "20th octo 2018"
        }
        response = self.client.post(
            "/api/v1/rides", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(response.status_code, 201)

    def test_user_can_request_a_ride(self):
        token = self.get_user_token()

        data = {
        }

        response = self.client.post(
            "/api/v1/rides/1/requests", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 201)
