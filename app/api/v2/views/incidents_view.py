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
