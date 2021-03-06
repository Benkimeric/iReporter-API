from db_config import db_connection
from flask import jsonify
import psycopg2
import os
import smtplib
import re
from .record_models import *
types_of_statuses = ["under investigation", "rejected", "resolved", "draft"]
types_or_record = ["red-flag", "intervention"]


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

    def get_all_interventions(self, type):
        """gets all the intervention records"""

        query = "SELECT * FROM incidents WHERE type = %s;"

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type,))
        incident_data = cur.fetchall()

        if len(incident_data) == 0:
            return{
                "message": "No " + type + " records available",
                "status": 404
                }, 404

        incidents_list = []
        for incident in incident_data:
            incidents_dict = {
                "id": incident[0],
                "created on": str(incident[1]),
                "created by": str(incident[2]),
                "type": incident[3],
                "location": incident[4],
                "status": incident[5],
                "comment": incident[6],
                "images": incident[7],
                "video": incident[8]
            }

            incidents_list.append(incidents_dict)

        return {
                "status": 200,
                "data": incidents_list
            }, 200

    def get_one_incident(self, type, incident_id):
        """gets a single intervention record"""

        query = self.incident_fetch()

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type, incident_id,))
        intervention_data = cur.fetchone()

        if intervention_data is None:
            return {
                "status": 404,
                "message": "This " + type + " record does not exist"
            }, 404

        intervention_dict = {
            "id": intervention_data[0],
            "create_on": str(intervention_data[1]),
            "create_by": str(intervention_data[2]),
            "type": intervention_data[3],
            "location": intervention_data[4],
            "status": intervention_data[5],
            "comment": intervention_data[6],
            "images": intervention_data[7],
            "video": intervention_data[8]
        }

        return {
            "status": 200,
            "data": intervention_dict
        }

    def delete_intervention(self, type, incident_id, user):
        """deletes intervention record"""
        query = self.incident_fetch()

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type, incident_id,))
        intervention_data = cur.fetchone()

        if intervention_data is None:
            return {
                "status": 404,
                "message": "This " + type + " record does not exist"
            }, 404

        # fetch creator
        cur.execute(query, (type, incident_id,))
        record_data = cur.fetchone()
        creator = record_data[2]
        record_status = record_data[5]

        # check user from logged in one
        user_data = self.check_user(user)
        user_id = user_data[0]

        if user_id != creator:
            return {
                "status": 403,
                'message': 'You can not delete other peoples records!'
            }, 403

        if record_status in types_of_statuses[:-1]:
            return {
                "status": 403,
                'message': 'You can not delete this record, it '
                'is already ' + record_status
            }, 403

        del_query = "DELETE FROM incidents WHERE type = %s AND \
                    incident_id =%s;"

        sql_del = del_query
        cur.execute(sql_del, (type, incident_id,))
        conn.commit()
        return {
            "id": incident_id,
            "message": type + " has been deleted",
            "status": 200
        }, 200

    def update_intervention(self, type, incident_id, user, comment):
        """updates intervention comment"""

        query = self.incident_fetch()

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type, incident_id,))
        intervention_data = cur.fetchone()

        if intervention_data is None:
            return {
                "status": 404,
                "message": "This " + type + " record does not exist"
            }, 404

        # fetch creator
        cur.execute(query, (type, incident_id,))
        record_data = cur.fetchone()
        creator = record_data[2]
        record_status = record_data[5]

        user_data = self.check_user(user)
        user_id = user_data[0]

        if user_id != creator:
            return {
                "status": 403,
                'message': 'You can not edit other peoples records!'
            }, 403

        if record_status in types_of_statuses[:-1]:
            return {
                "status": 403,
                'message': 'You can not edit this record, it '
                'is already ' + record_status
            }, 403

        update_query = "UPDATE incidents SET comment = %s WHERE type = %s AND\
         incident_id = %s;"

        sql_update = update_query
        cur.execute(sql_update, (comment, type, incident_id,))
        conn.commit()
        # updated record
        sql = self.incident_fetch()
        cur.execute(sql, (type, incident_id,))
        updated_data = cur.fetchone()

        incident_dict = {
            "created by": str(updated_data[2]),
            "type": updated_data[3],
            "location": updated_data[4],
            "status": updated_data[5],
            "comment": updated_data[6]
        }
        return {
            "id": incident_id,
            "status": 200,
            "message": "Updated " + type + " records comment",
            "data": incident_dict
        }, 200

    def incident_fetch(self):
        """fetches type and id of an incident"""

        sql = "SELECT * FROM incidents WHERE type = %s\
         and incident_id = %s;"
        return sql

    def check_user(self, user_id):
        conn = db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM users WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user_data = cur.fetchone()
        return user_data
