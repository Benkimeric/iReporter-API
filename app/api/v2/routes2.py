
from ..v2.views.users_view import UsersView, OneUser
from ..v2.views.incidents_view import IncidentViews, OneIntervention,\
    EditComment, EditLocation, ChangeStatus
from flask_restful import Api, Resource
from flask import Blueprint


version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2/')
api = Api(version_two)

api.add_resource(UsersView, 'auth/signup')
api.add_resource(OneUser, 'auth/login')

api.add_resource(IncidentViews, '<type>s')
api.add_resource(OneIntervention, '<type>s/<incident_id>')
api.add_resource(EditComment, '<type>s/<incident_id>/comment')
