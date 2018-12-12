from db_config import db_connection
from flask import jsonify
import psycopg2
import os


class Incidents():
    """contains methods for incidents"""

    def __init__(self):
        """initialises the incidents class"""
        self.db = db_connection()

    def save_incident(self, created_by, record_type, location, status, comment,
                      images, video):
        """saves incident record to the database"""

        query = "INSERT INTO incidents(created_by, type, location,\
        status, comment, images, video) VALUES \
        (%s,%s,%s,%s,%s,%s,%s) RETURNING incident_id"

        conn = db_connection()
        cur = conn.cursor()

        try:
            cur.execute(query, (
                created_by, record_type, location, status, comment,
                images, video
                ))
            new_record = cur.fetchone()
            conn.commit()
            return {
                "status": 201,
                "data": [
                    {
                        "message": "Created " + record_type + " record",
                        "id": new_record[0]
                    }
                ]
            }, 201
        except Exception as error:
            print(error)
            return jsonify({"message": "Error while saving Incident"})
