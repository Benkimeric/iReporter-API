from flask_restful import Resource
from flask import jsonify, request
from flask_restful import reqparse
from .validation import Validation
from flask_jwt_extended import jwt_required, get_jwt_identity
import re
from .record_views import *

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

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

        args = parser.parse_args()
        data = request.get_json()
        # validate input
        if Validation(data).check_incident_data():
            return Validation(data).check_incident_data()

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

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

        return self.incidents.get_all_interventions(type)


class OneIntervention(Resource, Incidents):
    """class to hold methods for a single intervention records"""

    def __init__(self):
        self.incidents = Incidents()

    @jwt_required
    def get(self, type, incident_id):
        """gets a single intervention record by id"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
            }, 400

        return self.incidents.get_one_incident(type, incident_id)

    @jwt_required
    def delete(self, type, incident_id):
        """deletes existing intervention record"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

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

    @jwt_required
    def patch(self, type, incident_id):
        """updates incident record comment"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

        if incident_id.isdigit() is False:
            return {
                "status": 400,
                'message': type + ' ID {} is invalid'.format(incident_id)
            }, 400

        args = parser_patch_c.parse_args()
        data = request.get_json()

        comment = data['comment']
        user = get_jwt_identity()

        if not re.match(r"^[a-zA-Z0-9 \"!?.,-]+$", data['comment']
                        ) or data['comment'].isspace():
            return {
                "status": 400,
                "message": "A comment cannot contain special characters e.g $ "
                           "or empty space"
            }, 400

        return self.incidents.update_intervention(
            type, incident_id, user, comment)


parser_patch_l = reqparse.RequestParser(bundle_errors=True)
parser_patch_l.add_argument(
    'location', type=str,
    required=True,
    help="Location cannot be left blank"
)


class EditLocation(Resource, Incidents2):
    """contains method to edit an incident record"""

    def __init__(self):
        """Initialises the editlocation class"""

        self.incidents = Incidents2()

    @jwt_required
    def patch(self, type, incident_id):
        """updates incident record location"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

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
                r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
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


class ChangeStatus(Resource, Incidents2):
    """contains method to edit an incident record"""

    def __init__(self):
        """Initialises the ChangeInterStatus class"""

        self.incidents = Incidents2()

    # only for admins
    @jwt_required
    def patch(self, type, incident_id):
        """updates incident record status"""

        if Validation(type).validate_type(type):
            return Validation(type).validate_type(type)

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
