import psycopg2
import os
from app.api.v2.models.db_model import Database
from instance.config import app_config
env = os.getenv('FLASK_ENV')
url = app_config[env].DATABASE_URL


def db_connection():
    """Create Database Connection"""

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


def create_super_admin():
    """create a default admin"""

    connection = db_connection()
    cursor = connection.cursor()

    database = Database()
    sql = database.add_admin()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
