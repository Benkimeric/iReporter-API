from flask_restful import Resource
from flask import jsonify, request
from flask_restful import reqparse
from .validation import Validation
from flask_jwt_extended import jwt_required, get_jwt_identity
import re

from ..models.incidents_model import Incidents2


class UserIncidents(Resource, Incidents2):

    def __init__(self):
        self.incidents = Incidents2()

    @jwt_required
    def get(self, type):
        """fetches a list of incident records by a specific user"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)
        user = get_jwt_identity()
        return self.incidents.get_user_records(type, user)


class IncidentsCount(Resource, Incidents2):

    def __init__(self):
        self.incidents = Incidents2()

    @jwt_required
    def get(self, type):
        """fetches a count of incident records by a specific user"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)
        user = get_jwt_identity()

        data = request.get_json()
        status = data['status']
        return self.incidents.count_incidents(user, type, status)
