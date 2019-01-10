from db_config import db_connection
from flask import jsonify
import psycopg2
import os
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


class Users():
    """holds methods for users models"""

    def __init__(self):
        """initialises the users class"""
        self.db = db_connection()

    def save_user(self, first_name, last_name, other_names,
                  user_name, email, phone_number, is_admin,
                  password):

        save_query = "INSERT INTO users(first_name, last_name, other_names,\
        username, email, phone_number, is_admin, password) VALUES \
        (%s,%s,%s,%s,%s,%s,%s,%s)"

        conn = db_connection()
        cur = conn.cursor()

        sql = self.get_by_username()
        cur.execute(sql, (user_name,))
        username_data = cur.fetchone()

        if username_data is not None:
            return {
                "status": 409,
                "message": "A user with this username exists"
            }, 409

        email_sql = self.check_email()
        cur.execute(email_sql, (email,))
        data = cur.fetchone()

        if data is not None:
            return {
                "status": 409,
                "message": "A user with this email already exists"
            }, 409

        phone_sql = self.check_phone()
        cur.execute(phone_sql, (phone_number,))
        phone_data = cur.fetchone()

        if phone_data is not None:
            return {
                "status": 409,
                "message": "A user with this phone number already exists"
            }, 409

        try:
            cur.execute(save_query, (first_name, last_name, other_names,
                                     user_name, email, phone_number, is_admin,
                                     password))
            conn.commit()
            # get saved user
            u_name_sql = self.get_by_username()
            cur.execute(u_name_sql, (user_name,))
            new_data = cur.fetchone()

            new_user_id = new_data[0]
            users_dict = {
                "user id": new_data[0],
                "first name": new_data[1],
                "last name": new_data[2],
                "other names": new_data[3],
                "user name": new_data[4],
                "email": new_data[5],
                "phone": new_data[6]
            }

            return {
                "status": 201,
                "data":
                    {
                        "user": users_dict
                    }
            }, 201

        except Exception as error:
            print(error)
            return jsonify({"message": "Error when saving user"})

    def login_user(self, username, password):
        """logs in user to the system"""
        conn = db_connection()
        cur = conn.cursor()

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
        if not check_password_hash(username_data[9], password):
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
            "data": [
                {
                    "token": access_token,
                    "user ID": id_of_user,
                    "username": u_name,
                    "first name": f_name,
                    "last name": l_name,
                    "other names": o_name,
                    "phone": phone,
                    "email": email,
                    "admin": admin
                }
            ]
        }, 200

    def make_admin(self, user, logged_user):
        """makes a normal user admin"""
        conn = db_connection()
        cur = conn.cursor()

        # fetch the user_id
        sql = self.get_by_id()
        cur.execute(sql, (user,))
        data = cur.fetchone()
        if data is None:
            return{
                "status": 404,
                "message": "This user does not exist"
            }, 404

        # check if user is admin
        user_sql = "SELECT * FROM users WHERE user_id = %s"
        cur.execute(user_sql, (logged_user,))
        user_data = cur.fetchone()
        user_role = user_data[7]

        if user_role is False:
            return {
                "status": 403,
                "message": "This action is only allowed to admins"
            }, 403

        try:
            query = "UPDATE users SET is_admin = True WHERE user_id = %s"
            # update the user
            cur.execute(query, (user,))
            conn.commit()
            return {
                "message": 'Successfully promoted user with ID {} to admin'
                .format(user),
                "status": 200
            }, 200

        except Exception as error:
            print(error)
            return jsonify({"message": "Error when promoting the user"})

    def get_by_username(self):
        """gets registered user by their name"""

        query = "SELECT * FROM users WHERE username = %s"
        return query

    def check_email(self):
        """fetches a user by email"""

        query = "SELECT * FROM users WHERE email = %s"
        return query

    def check_phone(self):
        """fetches a user by phone number"""

        query = "SELECT * FROM users WHERE phone_number = %s"
        return query

    def get_by_id(self):
        """gets registered user by their id"""

        query = "SELECT * FROM users WHERE user_id = %s"
        return query

    def view_users(self):
        sql = "SELECT * FROM users"
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        users_data = cur.fetchall()
        if users_data is None:
            return {
                "status": 404, "message": "There are no registered users"
            }, 404
        users_list = []
        for user in users_data:
            users_dict = self.user_dict(user)
            users_list.append(users_dict)
        return {
            "status": 200, "data": users_list
        }, 200

    def view_one_user(self, user):
        query = self.get_by_id()
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(query, (user,))
        user_data = cur.fetchone()
        if user_data is None:
            return {
                "status": 404, "message": "This user does not exist"
            }, 404
        return {
            "status": 200, "data": self.user_dict(user_data)
        }, 200

    def user_dict(self, user_data):
        user_dict = {
            "id": user_data[0], "first_name": str(user_data[1]),
            "last_name": str(user_data[2]), "other_names": user_data[3],
            "user_name": user_data[4], "email": user_data[5],
            "phone": user_data[6], "is_admin": user_data[7]
        }
        return user_dict
