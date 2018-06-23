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
                "email": "jamesmasher@gmail.com",
                "password": "qwerty",
                "permission": "1"
            },

            "login-cred": {
                "email": "jamesmasher@gmail.com",
                "password": "qwerty"
            }
        }

    def tearDown(self):
        pass

    def test_signup(self):
        response = self.client.post(
            "/api/v1/auth/signup", data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post(
            "/api/v1/auth/login", data=json.dumps(self.data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/api/v1/auth/login", data=json.dumps(self.data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)

    def test_non_existing_user(self):
        response = self.client.post(
            "/api/v1/auth/signup", data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        data = {
            "email": "johnokum@gmail.com",
            "password": "password"
        }
        response = self.client.post(
            "/api/v1/auth/login", data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 401)
