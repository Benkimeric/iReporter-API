
from .views.red_flags_view import Records, OneRecord, EditComment,EditLocation


from flask_restful import Api,Resource
from flask import Blueprint


version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1/')
api = Api(version_one)

api.add_resource(Records, 'red-flags')
api.add_resource(OneRecord, "red-flags/<int:records_id>")
api.add_resource(EditComment, "red-flags/<int:records_id>/comment")
api.add_resource(EditLocation, "red-flags/<int:records_id>/location")
