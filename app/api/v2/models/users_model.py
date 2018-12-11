from db_config import db_connection
from flask import jsonify
import psycopg2
import os


class Users():
    """holds methods for users models"""

    def __init__(self):
        """initialises the users class"""
        self.db = db_connection()

    def save_user(self):

        query = "INSERT INTO users(first_name, last_name, other_names,\
        username, email, phone_number, is_admin, password) VALUES \
        (%s,%s,%s,%s,%s,%s,%s,%s)"

        return query

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
