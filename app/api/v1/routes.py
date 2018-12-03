
from .views.red_flags_view import Records, OneRecord, EditComment,EditLocation
from ..v1.views.users_view import Users, OneUser,Login

from flask_restful import Api,Resource
from flask import Blueprint


version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1/')
api = Api(version_one)

api.add_resource(Records, 'red-flags')
api.add_resource(OneRecord, "red-flags/<int:records_id>")
api.add_resource(EditComment, "red-flags/<int:records_id>/comment")
api.add_resource(EditLocation, "red-flags/<int:records_id>/location")

#for users
api.add_resource(Users, 'users')
api.add_resource(OneUser, 'users/<int:user_id>') 

#login
api.add_resource(Login, 'users/auth/login')