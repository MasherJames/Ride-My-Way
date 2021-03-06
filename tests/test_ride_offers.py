from ..app import create_app
import unittest
import json
from ..db_tables import create_tables, drop_tables


class TestRideOffers(unittest.TestCase):

    def setUp(self):
        '''
        Setup the app to testing mode
        creating a test client for testing
        '''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.data = {
            "signup-cred": {
                "username": "Macharia",
                "email": "mash@gmail.com",
                "password": "Qwerty123",
                "permission": "1"
            },
            "login-cred": {
                "username": "Macharia",
                "password": "Qwerty123"
            }
        }

    def tearDown(self):
        '''Drop  the tables after test'''
        drop_tables()
        self.app_context.pop()

    def signup(self):
        '''Sign up function'''

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        ''' Login function '''
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.data['login-cred']),
            headers={'content-type': 'application/json'}
        )

        return response

    '''
    Test if a user can successfully signup
    '''

    '''
    Test a user can successfully login after creating an account
    '''

    def test_login(self):
        '''
        Test a user can successfully login after creating an account
        '''
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

    def test_username_exists(self):
        '''
        Test username is already in use at the time of creating an accout
        '''
        self.signup()
        response = self.signup()

        self.assertEqual(response.status_code, 400)

    def test_email_exists(self):
        '''
        Test email is already in use
        '''
        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(dict(
                username="dannydan",
                email="james@gmail.com",
                password="Passwrd123",
                permission="1"
            )),
            headers={'content-type': 'application/json'}
        )

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(dict(
                username="kimkush",
                email="james@gmail.com",
                password="Kimkush123",
                permission="1"
            )),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_credentials(self):
        '''
        Test invalid input data during signup
        '''

        data = {
            'username': ' ',
            'email': 'kim.kim',
            'password': 'Password123'
        }

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def get_user_token(self):
        '''
        Get token function
        '''

        self.signup()
        response = self.login()
        token = json.loads(response.data).get('token', None)

        return token

    def test_user_get_token(self):
        '''
        Test a user gets a token after login
        '''
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

        self.assertIn('token', json.loads(response.data))

    def test_user_can_view_all_ride_offers(self):
        '''
        Test a logged in user can view all ride offers
        '''
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_a_specific_ride_offer(self):
        '''
        Test a user can view the details of a specific ride when logged in
        '''
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides/1",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_ride_offer(self):
        '''
        Test a logged in user can create a ride offer
        '''
        token = self.get_user_token()

        data = {
            "from": "Nakuru",
            "to": "ruiru",
            "depature": "20thAugust2018"
        }
        response = self.client.post(
            "/api/v1/users/rides", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(response.status_code, 201)

    def test_user_can_request_a_ride(self):
        '''
        Test user can request to join a ride offer
        '''
        token = self.get_user_token()

        data = {
        }

        response = self.client.post(
            "/api/v1/rides/1/requests", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 201)
