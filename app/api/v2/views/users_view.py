from flask_restful import Resource
from flask import jsonify, request
from ...v2.models.users_model import Users
from flask_restful import reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import re


is_admin = False

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('first_name', type=str, required=True,
                    help="First name field is required")

parser.add_argument('last_name', type=str, required=True,
                    help="Last name field is required")
parser.add_argument('other_names', type=str, required=True,
                    help="Other names field is required")

parser.add_argument('email', type=str, required=True,
                    help="Email field is required")

parser.add_argument('phone_number', type=str, required=True,
                    help="Phone field is required")

parser.add_argument('user_name', type=str, required=True,
                    help="User name field is required")

parser.add_argument('password', type=str, required=True,
                    help="Password field is required")
parser.add_argument('confirm_password',
                    help='Confirm password field is required',
                    required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('user_name', help='Username field is required',
                     required=True)
parser2.add_argument('password', help='Password field is required',
                     required=True)


class UsersView(Resource, Users):
    """class to hold methods for users"""
    def __init__(self):
        self.user = Users()

    def post(self):

        data = parser.parse_args()
        data = request.get_json()

        if data['first_name'].isalpha() is False:
            return {'message': 'Please enter a valid First name'}, 400

        if data['last_name'].isalpha() is False:
            return {'message': 'Please enter a valid Last name'}, 400

        if data['other_names'].isalpha() is False:
            return {
                'message': 'Please enter a valid value for other names'
                }, 400

        if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)",
                        data['email']):
            return {"message": "Please provide a valid email address"}, 400

        if not re.match(r"(^07\d{8}$)", data['phone_number']):
            return {
                "message": "Please provide a valid phone number"
                " e.g 0727423XXX"
                }, 400

        if not re.match(r"(^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$)",
                        data['password']):
            return {"message": "password min length is 8 characters, at least "
                    "1 letter, 1 number and a special character"}, 400

        if data['password'] != data['confirm_password']:
            return {"message": "passwords do not match", "status": 400}, 400

        if not re.match(r"(^[a-zA-Z0-9]*$)", data['user_name']):
            return {
                "message": "please enter a valid username",
                "status": 400
                }, 400

        first_name = str(data['first_name']).lower()
        last_name = str(data['last_name']).lower()
        other_names = str(data['other_names']).lower()
        email = str(data['email']).lower()
        phone_number = data['phone_number']
        user_name = str(data['user_name']).lower()
        password = generate_password_hash(data['password'])

        return self.save_user(first_name, last_name, other_names,
                              user_name, email, phone_number, is_admin,
                              password)


class OneUser(Resource, Users):
    """class to hold user login method"""

    def post(self):
        """logs in a user to the system"""

        data = parser2.parse_args()
        username = str(data['user_name']).lower()
        password = data['password']

        return self.login_user(username, password)


class MakeAdmin(Resource, Users):
    """class to hold user make admin"""

    @jwt_required
    def patch(self, user_id):
        """makes a user admin"""

        if user_id.isdigit() is False:
            return {
                "status": 400,
                'message': 'ID {} is invalid'.format(user_id)
                }, 400
        logged_user = get_jwt_identity()
        return self.make_admin(user_id, logged_user)


class ViewAllUsers(Resource, Users):
    """class to hold view users method"""

    @jwt_required
    def get(self):
        """view all users"""

        return self.view_users()


class ViewOneUser(Resource, Users):
    """class to hold view single user method"""

    @jwt_required
    def get(self, user_id):
        """view single user"""

        return self.view_one_user(user_id)
