from app import app
import unittest
import json


class TestRideOffers(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.data = {
            "signup-cred": {
                "fullname": "james macharia",
                "email": "jamesmasher@gmail.com",
                "password": "qwerty",
                "repeat-password": "qwerty"
            },

            "login-cred": {
                "email": "jamesmasher@gmail.com",
                "password": "qwerty"
            }
        }

    def tearDown(self):
        pass

    def signup(self):
        response = self.client.post(
            "/api/v1/auth/signup/", data=json.dumps(self.data['signup-cred']),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

    def login(self):
        response = self.client.post(
            "/api/v1/auth/signup/", data=json.dumps(self.data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/api/v1/auth/login/", data=json.dumps(self.data),
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
