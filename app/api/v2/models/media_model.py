from db_config import db_connection
from flask import jsonify
import psycopg2

types_of_statuses = ["under investigation", "rejected", "resolved", "draft"]


class IncidentsMedia():
    """contains methods for incidents"""

    def __init__(self):
        """initialises the incidents class"""
        self.db = db_connection()

    def add_image(self, media, type, incident_id, file_path):
        """updates incident with image"""

        query = "SELECT * FROM incidents WHERE type = %s\
         and incident_id = %s;"

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query, (type, incident_id,))
        intervention_data = cur.fetchone()
        record_status = intervention_data[5]

        if intervention_data is None:
            return {
                "status": 404,
                "message": "This " + type + " record does not exist"
            }, 404

        if record_status in types_of_statuses[:-1]:
            return {
                "status": 403,
                'message': 'You can not edit this record, it '
                'is already ' + record_status
            }, 403

        update_query = "UPDATE incidents SET "+media+" = %s WHERE type = %s AND\
         incident_id = %s;"

        try:
            sql_update = update_query
            cur.execute(sql_update, (file_path, type, incident_id,))
            conn.commit()
            # updated record
            sql = "SELECT * FROM incidents WHERE type = %s\
                    and incident_id = %s;"
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
                "message": "Added " + media + " to " + type + " record",
                "data": incident_dict
            }, 200
        except Exception as error:
            print(error)
            return jsonify({'message': 'Error adding file'})
