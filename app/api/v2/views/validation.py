import re

types_or_record = ["red-flag", "intervention"]


class Validation():

    def __init__(self, data):
        self.data = data

    def check_incident_data(self):
        """checks the type of incident record"""
        if not re.match(r"^[a-zA-Z0-9 \"!?.,-]+$", self.data['comment']
                        ) or self.data['comment'].isspace():
            return {
                "message": "A comment cannot contain special characters e.g $ "
                           "or empty space"
                }, 400

        if self.data['record_type'] not in map(str.lower, types_or_record):
            return {
                "message": "Record type can only be a red-flag or an "
                "intervention", "status": 400
                }, 400

        if not re.match(
                r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
                self.data['location']
                ):
            return {
                "message": "Please ensure comma separated lat and long and "
                "within appropriate ranges", "status": 400}, 400

    def validate_type(self, type):
        """checks type to be only red-flag and intervention"""

        if type not in map(str.lower, types_or_record):
            return {
                "message": "Check URL, record type can only be a "
                "red-flag or intervention",
                "status": 400
                }, 400
