from db_config import db_connection
from flask import jsonify
import psycopg2
import os
import smtplib
import re

types_of_statuses = ["under investigation", "rejected", "resolved", "draft"]
types_or_record = ["red-flag", "intervention"]


class Incidents2():
    """contains more methods for incidents"""

    def __init__(self):
        """initialises the incidents class"""
        self.db = db_connection()

    def count_incidents(self, user, type, status):
        """saves incident record to the database"""

        query = "SELECT COUNT(*) FROM incidents WHERE created_by=%s\
         and type=%s and status=%s;"

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (user, type, status))
        count = cur.fetchall()
        conn.commit()
        return {
            "status": 200,
            "count": count
        }, 200

    def get_user_records(self, type, user):
        """gets all the incident records by specific user"""

        query = "SELECT * FROM incidents WHERE type = %s and created_by = %s;"

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type, user,))
        incident_data = cur.fetchall()

        if len(incident_data) == 0:
            return{
                "message": "You haven't created any " + type + " records",
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

    # cut from incidents model to reduce file size
    def update_intervention_location(self, type, incident_id, user, location):
        """updates intervention location"""

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

        try:
            sql_update = "UPDATE incidents SET location = %s WHERE type = %s AND\
                            incident_id = %s;"
            cur.execute(sql_update, (location, type, incident_id,))
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
                'message': 'Updated ' + type + ' records location',
                "data": incident_dict
            }
        except Exception as error:
            print(error)
            return jsonify({'message': 'Error updating ' + type + ' location'})

    def update_status(self, type, incident_id, user, status):
        """updates incident status"""
        sql = self.incident_fetch()

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(sql, (type, incident_id,))
        intervention_data = cur.fetchone()

        if intervention_data is None:
            return {
                "status": 404,
                "message": "This " + type + " record does not exist"
            }, 404

        if status not in map(str.lower, types_of_statuses):
            return {
                "message": "Status can only be resolved, rejected or an "
                "under investigation", "status": 400
                }, 400

        # check creator details
        cur.execute(sql, (type, incident_id,))
        record_data = cur.fetchone()
        creator_id = record_data[2]

        creator_object = self.check_user(creator_id)
        creator_email = creator_object[5]

        # check if user is admin
        user_data = self.check_user(user)
        user_role = user_data[7]

        if user_role is False:
            return {
                "status": 403,
                "message": "This action is only allowed to admins"
            }, 403
        # check if admin edits their own
        if user == record_data[2]:
            return {
                "status": 403,
                "message": "You can not change status of your own record"
            }, 403

        try:
            sql_update = "UPDATE incidents SET status = %s WHERE type = %s AND\
                        incident_id = %s;"
            cur.execute(sql_update, (status, type, incident_id,))
            conn.commit()
            # send email
            FROM = "technologysolutions254@gmail.com"
            TO = creator_email
            SUBJECT = "Incident Record Status changed"
            MESSAGE = "Your {} record is now {}".format(type, status)
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(
                    "technologysolutions254@gmail.com", "benkimkimeueric")
                msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
                """ % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
                server.sendmail(FROM, TO, msg)
                server.quit()

            except:
                return jsonify({
                    "status": 200,
                    "message": "status set to {} ;could "
                    "not send email".format(status)
                })

            return {
                "status": 200,
                "id": incident_id,
                "message": "Updated " + type + " record status"
            }, 200
        except Exception as error:
            print(error)
            return jsonify({"message": "Error updating " + type + " status"})

    def check_user(self, user_id):
        conn = db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM users WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user_data = cur.fetchone()
        return user_data

    def incident_fetch(self):
        """fetches type and id of an incident"""

        sql = "SELECT * FROM incidents WHERE type = %s\
         and incident_id = %s;"
        return sql

    def get_email(self, user_id):
        conn = db_connection()
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user_data = cur.fetchone()
