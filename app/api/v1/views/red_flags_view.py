from flask_restful import Resource
from flask import jsonify, make_response, request

# local import
from ..models.red_flags_model import Incidences, records_list


class Records(Resource, Incidences):
    def __init__(self):
        self.db = Incidences()

    def post(self):
        data = request.get_json()
        created_by = data['created_by']
        record_type = data['record_type']
        location = data['location']
        comment = data['comment']

        # return make_response(jsonify({"My new Friend list": resp}), 201)
        if comment == "" or not comment:
            return {"message": "Please fill all the required fields", "status": 400}, 400

        resp = self.db.save(created_by, record_type, location, comment)
        return {
                "status": 201,
                "data": [
                    {
                        "id": resp["record_id"],
                        "message": "created red-flag record"

                    }
                ]
            }, 201

    def get(self):
        resp = self.db.get_all_records()
        if len(resp) == 0:
            return {"message": "There are no records available", "status": 200},200
        return {
                "status": 200,
                "data": resp
            },200


class OneRecord(Resource, Incidences):
    def __init__(self):
        # self.db = Incidences()
        pass

    def get(self, records_id):
        record = self.get_one_record(records_id)
        if len(record) == 0:
            return {"message": "There is no record with this ID", "status": 404},404
        else:
            return {"Record data": record, "status": 200},200

    def delete(self, records_id):
        """Delete a record"""
        record = self.get_one_record(records_id)
        if len(record) == 0:
            return {"message": "No record with this ID", "status": 404},404


        records_list.remove(record[0])

        return {
                "status": 200,
                "data": [
                    {
                        "id": records_id,
                        "message": "Red-flag record has been deleted"
                    }
                ]
            },200


class EditComment(Resource, Incidences):
    def __init__(self):
        pass

    def patch(self, records_id):
        """updates Record data"""
        record = self.get_one_record(records_id)

        if len(record) == 0:
            return {"message": "No record with this ID", "status": 404},404

        data = request.get_json()

        comment = data['comment']

        index = self.get_index(records_id)

        data = {
            "comment": comment,
            "index": index
        }

        self.update_record(**data)

        return {
                "data": [
                    {
                        "status": 200,
                        "message": "Updated red-flag record's comment"
                    }
                ]
            },200


class EditLocation(Resource, Incidences):
    def __init__(self):
        pass

    def patch(self, records_id):
        """updates Location record data"""
        record = self.get_one_record(records_id)

        if len(record) == 0:
            return jsonify({"message": "No record with this ID", "status": 404})

        data = request.get_json()

        location = data['location']

        index = self.get_index(records_id)

        data = {
            "location": location,
            "index": index
        }

        self.update_record_location(**data)

        return {
                "status": 200,
                "data": [
                    {
                        "id": records_id,
                        "message": "Updated red-flag record's Location"

                    }
                ]

            },200
