import unittest
from flask import json
from app.api.v2.models.db_model import Database
from db_config import db_connection
from app import create_app, create_tables
from .data import *


class Registration(unittest.TestCase):
    """contains test cases for signup and login"""

    def setUp(self):
        """ Define tests variables"""

        create_tables()
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

    def tearDown(self):
        """teardown method to clear database"""
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        cursor.execute("DROP TABLE IF EXISTS incidents CASCADE")
        connection.commit()

    def test_can_register(self):
        """test if can create a new user"""
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(201, response.status_code)

    def test_throws_eror_with_invalid_email(self):
        """test registratiion with invalid email"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data_fake_email),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'Please provide a '
                         'valid email address')

    def test_throws_eror_with_invalid_phone(self):
        """test registratiion with invalid phone"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_invalid_phone),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'Please provide a valid '
                         'phone number e.g 0727423XXX')

    def test_throws_eror_with_invalid_first_name(self):
        """test registratiion with invalid first name"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(invalid_f_name),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'Please enter a valid First name')

    def test_throws_eror_with_invalid_last_name(self):
        """test registratiion with invalid last name"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(invalid_l_name),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'Please enter a valid Last name')

    def test_throws_eror_with_invalid_other_name(self):
        """test registratiion with invalid other name"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(invalid_o_name),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            result['message'], 'Please enter a valid value for other names')

    def test_throws_error_duplicate_username(self):
        """test with existing username"""

        # signup user
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # signup user again
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # test
        self.assertEqual(409, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['message'], 'A user with this username exists')

    def test_throws_error_on_existing_phone(self):
        """test with existing phone number"""

        # signup user 1
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # signup user 2
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(existing_phone),
            content_type='application/json')
        # test
        self.assertEqual(409, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['message'], 'A user with this phone number already exists')

    def test_throws_error_on_existing_email(self):
        """test with existing username"""

        # signup user 1
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # signup user 2
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(existing_email),
            content_type='application/json')
        # test
        self.assertEqual(409, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['message'], 'A user with this email already exists')

    # login tests
    def test_user_can_login(self):
        """test case for user login"""
        # create user
        self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # login user
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(sign_in_data),
            content_type='application/json')
        # test
        self.assertEqual(200, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['status'], 200)

    def test_login_with_wrong_username(self):
        """tests returns error on invalid username"""

        # create user
        self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # login user
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(invalid_username),
            content_type='application/json')
        # test
        self.assertEqual(401, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['message'], 'You have entered wrong username or password')

    def test_login_with_wrong_password(self):
        """tests returns error on wrong password"""

        # create user
        self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # login user
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(wrong_phone),
            content_type='application/json')
        # test
        self.assertEqual(401, response.status_code)
        result = json.loads(response.data)
        self.assertEqual(
            result['message'], 'You have entered wrong username or password')

    def test_valid_password_length(self):
        """test registratiion with invalid password length"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(password_data),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'password min length is '
                         '8 characters, at least 1 letter, 1 number and a '
                         'special character'
                         )

    def test_throws_error_on_invalid_username(self):
        """test registratiion with invalid username"""

        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(wrong_username),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'please enter a valid username')

    def test_throws_error_on_no_match_passwords(self):
        """test that cannot register with non match in passwords"""
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_with_no_match_password),
            content_type='application/json')
        result = json.loads(response.data)
        print(result)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'passwords do not match')
