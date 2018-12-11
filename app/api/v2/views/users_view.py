from flask_restful import Resource
from flask import jsonify, request
from ...v2.models.users_model import Users
from flask_restful import reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity
import re

from ...v2.models import users_model

from db_config import db_connection
from flask import jsonify
import psycopg2
import os

is_admin = False

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('first_name', type=str, required=True,
                    help="first name cannot be left blank")

parser.add_argument('last_name', type=str, required=True,
                    help="Last name cannot be left blank")
parser.add_argument('other_names', type=str, required=True,
                    help="Other name cannot be left blank")

parser.add_argument('email', type=str, required=True,
                    help="email cannot be left blank")

parser.add_argument('phone_number', type=str, required=True,
                    help="Phone number cannot be left blank")

parser.add_argument('user_name', type=str, required=True,
                    help="User name cannot be left blank")

parser.add_argument('password', type=str, required=True,
                    help="password cannot be left blank")


class UsersView(Resource, Users):
    """class to hold methods for users"""
    def __init__(self):
        self.user = Users()

    def post(self):

        conn = db_connection()
        cur = conn.cursor()

        args = parser.parse_args()

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

        if not re.match(r"([+ 0-9]{13})", data['phone_number']):
            return {
                "message": "Please provide a valid phone number"
                " e.g +254727423942"
                }, 400

        first_name = data['first_name']
        last_name = data['last_name']
        other_names = data['other_names']
        email = data['email']
        phone_number = data['phone_number']
        user_name = data['user_name']
        password = data['password']

        sql = self.get_by_username()
        cur.execute(sql, (user_name,))
        username_data = cur.fetchone()

        if username_data is not None:
            return {
                "status": 409,
                "message": "A user with this username exists"
                }, 409

        sql = self.check_email()
        cur.execute(sql, (email,))
        data = cur.fetchone()

        if data is not None:
            return {
                "status": 409,
                "message": "A user with this email already exists"
                }, 409

        sql = self.check_phone()
        cur.execute(sql, (phone_number,))
        phone_data = cur.fetchone()

        if phone_data is not None:
            return {
                "status": 409,
                "message": "A user with this phone number already exists"
                }, 409

        try:
            sql = self.user.save_user()
            cur.execute(sql, (first_name, last_name, other_names, user_name,
                              email, phone_number, is_admin, password))
            conn.commit()
            # get saved user
            sql = self.get_by_username()
            cur.execute(sql, (user_name,))
            new_data = cur.fetchone()

            new_user_id = new_data[0]
            users_dict = {
                "first name": new_data[1],
                "last name": new_data[2],
                "other names": new_data[3],
                "user name": new_data[4],
                "email": new_data[5],
                "phone": new_data[6]
            }

            access_token = create_access_token(identity=new_user_id)
            return {
                "status": 201,
                "data": [
                    {
                        "token": access_token,
                        "user": users_dict
                    }
                ]
            }, 201
        except Exception as error:
            print(error)
            return jsonify({"message": "Error when saving user"})


class OneUser(Resource, Users):

    def post(self):
        """logs in a user to the system"""

        index_name = "user_name"
        index_pass = "password"

        conn = db_connection()
        cur = conn.cursor()

        data = parser2.parse_args()
        username = data['user_name']
        password = data['password']

        # fetch the username
        sql = self.get_by_username()
        cur.execute(sql, (username,))
        username_data = cur.fetchone()

        if username_data is None:
            return{
                "status": 401,
                "message": "You have entered wrong username or password"
                }, 401

        # check password
        if username_data[9] != password:
            return{
                "status": 401,
                "message": "You have entered wrong username or password"
                }, 401

        id_of_user = username_data[0]
        f_name = username_data[1]
        o_name = username_data[2]
        l_name = username_data[3]
        u_name = username_data[4]
        email = username_data[5]
        phone = username_data[6]
        admin = username_data[7]

        access_token = create_access_token(identity=id_of_user)
        return {
                "status": 200,
                "token": access_token,
                "data": [
                    {
                        "token": access_token,
                        "user ID": id_of_user,
                        "username": u_name,
                        "first name": f_name,
                        "last name": l_name,
                        "other names": o_name,
                        "phone": phone,
                        "email": email
                    }
                ]
            }, 200
