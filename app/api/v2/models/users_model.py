from db_config import db_connection
from flask import jsonify
import psycopg2
import os
from flask_jwt_extended import create_access_token, get_jwt_identity


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
