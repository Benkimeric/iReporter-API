
from ..v2.views.users_view import UsersView, OneUser, MakeAdmin, ViewAllUsers,\
    ViewOneUser
from ..v2.views.incidents_view import IncidentViews, OneIntervention,\
    EditComment, EditLocation, ChangeStatus, UserIncidents, IncidentsCount
from ..v2.views.media_views import UploadImage
from flask_restful import Api, Resource
from flask import Blueprint


version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2/')
api = Api(version_two)

api.add_resource(UsersView, 'auth/signup')
api.add_resource(OneUser, 'auth/login')
api.add_resource(MakeAdmin, 'makeadmin/<user_id>')
api.add_resource(ViewAllUsers, 'users')
api.add_resource(ViewOneUser, 'users/profile')

api.add_resource(IncidentViews, '<type>')
api.add_resource(OneIntervention, '<type>/<incident_id>')
api.add_resource(EditComment, '<type>/<incident_id>/comment')
api.add_resource(EditLocation, '<type>/<incident_id>/location')
api.add_resource(ChangeStatus, '<type>/<incident_id>/status')
api.add_resource(UserIncidents, 'user/<type>')
api.add_resource(IncidentsCount, 'user/<type>/<status>')
api.add_resource(UploadImage, '<type>/<incident_id>/<media>')
