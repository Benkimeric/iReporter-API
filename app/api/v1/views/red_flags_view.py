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
            return jsonify({"message": "You must provide a name", "status": 400})

        resp = self.db.save(created_by, record_type, location, comment)
        return jsonify({"data": resp, "message": "created red-flag record succeffuly", "status": 201})

    def get(self):
        resp = self.db.get_all_records()
        if len(resp) == 0:
            return jsonify({"message": "There are no records available", "status": 200})
        return jsonify({"data": resp, "status": 200})
