import unittest
from flask import current_app
from app import create_app


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        ''' create an app context for testing '''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        ''' destroy app context after testing is done '''
        self.app_context.pop()

    def test_app_exists(self):
        ''' testing for the presence of the app contest '''
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        ''' testing if the config mode is testing '''
        self.assertTrue(current_app.config['TESTING'])
