from app import create_app
import unittest
import json
from db_tables import create_tables, drop_tables


class TestRideOffers(unittest.TestCase):
    '''
    Setup the app to testing mode
    creating a test client for testing
    '''

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.client = self.app.test_client()
        self.data = {
            "signup-cred": {
                "username": "macharia",
                "email": "jamesmash@gmail.com",
                "password": "qwerty",
                "permission": "1"
            },
            "login-cred": {
                "username": "macharia",
                "password": "qwerty"
            }
        }

    '''
    drop  the tables after test
    '''

    def tearDown(self):
        drop_tables()

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

    '''
    Test if a user can successfully signup
    '''

    # def test_signup(self):
    #     response = self.signup()

    #     self.assertEqual(response.status_code, 201)

    '''
    Test a user can successfully login after creating an account
    '''

    def test_login(self):
        ''' signup a user first '''
        self.signup()
        response = self.login()

        self.assertEqual(response.status_code, 200)

    '''
    test username is already in use at the time of creating an accout
    '''

    def test_username_exists(self):
        self.signup()
        response = self.signup()

        self.assertEqual(response.status_code, 400)

    '''
    test email is already in use
    '''

    def test_email_exists(self):
        self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(dict(
                username="james",
                email="james@gmail.com",
                password="qwerty",
                permissions="1"
            )),
            headers={'content-type': 'application/json'}
        )

        response = self.client.post(
            "/api/v1/auth/signup",
            data=json.dumps(dict(
                username="mash",
                email="james@gmail.com",
                password="qwerty",
                permissions="1"
            )),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

    '''
    Test invalid input data during signup
    '''

    def test_invalid_credentials(self):
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

    '''
    get token function
    '''

    def get_user_token(self):
        self.signup()
        response = self.login()
        token = json.loads(response.data).get('token', None)

        return token

    '''
    Test a user gets a token after login
    '''

    def test_user_get_token(self):
        self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

        self.assertIn('token', json.loads(response.data))

    '''
    Test a logged in user can view all ride offers
    '''

    def test_user_can_view_all_ride_offers(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    '''
    Test a user can view the details of a specific ride when logged in
    '''

    def test_user_can_view_a_specific_ride_offer(self):
        token = self.get_user_token()

        response = self.client.get(
            "/api/v1/rides/1",
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )
        self.assertEqual(response.status_code, 200)

    '''
    Test a logged in user can create a ride offer
    '''

    def test_user_can_create_ride_offer(self):
        token = self.get_user_token()

        data = {
            "from": "Nakuru",
            "to": "ruiru",
            "depature": "20th octo 2018"
        }
        response = self.client.post(
            "/api/v1/users/rides", data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(response.status_code, 201)

    '''
    test user can request to join a ride offer
    '''

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
