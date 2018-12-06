import psycopg2
import os
from app.api.v2.models.db_model import Database


def db_connection():
    """Create Database Connection"""

    url = "dbname='ireporter' host='localhost' \
     port='5432' user='postgres'password='kali12'"

    connection = psycopg2.connect(url)
    return connection


def create_tables():
    """Creates the Tables"""

    connection = db_connection()
    cursor = connection.cursor()

    database = Database()
    queries = database.db_query()

    for sql in queries:
        cursor.execute(sql)
        connection.commit()

    cursor.close()
