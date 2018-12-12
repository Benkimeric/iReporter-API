from flask_restful import Resource
from flask import jsonify, request
from flask_restful import reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity
import re

from ..models.incidents_model import Incidents

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'comment', type=str,
    required=True,
    help="Comment cannot be left blank"
)

parser.add_argument(
    'location', type=str,
    required=True,
    help="Location cannot be left blank"
)

parser.add_argument(
    'record_type', type=str,
    required=True,
    help="Record Type cannot be left blank"
)

types_or_record = ["red-flag", "intervention"]


class IncidentViews(Resource, Incidents):
    """contains methods for incidents"""

    def __init__(self):
        self.incidents = Incidents()

    @jwt_required
    def post(self, type):
        """saves a new incident record"""

        args = parser.parse_args()

        data = request.get_json()

        type = data['record_type']

        if not re.match(r"^[a-zA-Z0-9 \"!?.,-]+$", data['comment']):
            return {
                "message": "A comment cannot contain special characters e.g $"
                }, 400

        if data['record_type'] not in map(str.lower, types_or_record):
            return {
                "message": "Record type can only be a red-flag or an "
                "intervention", "status": 400
                }, 400

        if not re.match(
                r"^([-+]?\d{1,2}([.]\d+)?),\s*([-+]?\d{1,3}([.]\d+)?)$",
                data['location']
                ):
            return {
                "message": "Please ensure comma separated lat and long and "
                "within appropriate ranges", "status": 400}, 400

        created_by = get_jwt_identity()
        record_type = data['record_type']
        location = data['location']
        comment = data['comment']
        status = "draft"
        images = []
        video = []

        return self.incidents.save_incident(created_by, record_type, location,
                                            status, comment, images, video)

    @jwt_required
    def get(self, type):
        """fetches a list of all the incident records by type"""

        return self.incidents.get_all_interventions(type)


class OneIntervention(Resource, Incidents):
    """class to hold methods for a single intervention records"""

    def __init__(self):
        self.incidents = Incidents()

    def get(self, type, incident_id):
        """gets a single intervention record by id"""

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
                }, 400

        return self.incidents.get_one_incident(type, incident_id)

    def delete(self, type, incident_id):
        """deletes existing intervention record"""

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
                }, 400

        user = get_jwt_identity()
        return self.incidents.delete_intervention(type, incident_id, user)

parser_patch_c = reqparse.RequestParser(bundle_errors=True)
parser_patch_c.add_argument(
        'comment', type=str,
        required=True,
        help="Comment cannot be left blank"
    )


class EditComment(Resource, Incidents):
    """contains method to edit an incident record"""

    def __init__(self):
        """Initialises the editcomment class"""

        self.incidents = Incidents()

    def patch(self, type, incident_id):
        """updates incident record comment"""

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
                }, 400

        args = parser_patch_c.parse_args()
        data = request.get_json()

        comment = data['comment']
        user = get_jwt_identity()

        if not re.match(r"^[a-zA-Z0-9 \"!?.,-]+$", data['comment']):
            return {
                "message": "A comment cannot contain special characters e.g $"
                }, 400

        return self.incidents.update_intervention(
            type, incident_id, user, comment)


parser_patch_l = reqparse.RequestParser(bundle_errors=True)
parser_patch_l.add_argument(
        'location', type=str,
        required=True,
        help="Location cannot be left blank"
    )


class EditLocation(Resource, Incidents):
    """contains method to edit an incident record"""

    def __init__(self):
        """Initialises the editlocation class"""

        self.incidents = Incidents()

    def patch(self, type, incident_id):
        """updates incident record location"""

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
                }, 400

        args = parser_patch_l.parse_args()
        data = request.get_json()

        location = data['location']
        user = get_jwt_identity()

        if not re.match(
                r"^([-+]?\d{1,2}([.]\d+)?),\s*([-+]?\d{1,3}([.]\d+)?)$",
                location
                ):
            return {
                "message": "Please ensure comma separated lat and long and "
                "within appropriate ranges", "status": 400}, 400

        return self.incidents.update_intervention_location(
            type, incident_id, user, location)


parser_patch_s = reqparse.RequestParser(bundle_errors=True)
parser_patch_s.add_argument(
        'status', type=str,
        required=True,
        help="Status cannot be left blank"
    )


class ChangeStatus(Resource, Incidents):
    """contains method to edit an incident record"""

    def __init__(self):
        """Initialises the ChangeInterStatus class"""

        self.incidents = Incidents()

    # only for admins
    @jwt_required
    def patch(self, type, incident_id):
        """updates incident record status"""

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
                }, 400

        args = parser_patch_s.parse_args()
        data = request.get_json()

        status = data['status']
        user = get_jwt_identity()

        return self.incidents.update_status(type, incident_id, user, status)
