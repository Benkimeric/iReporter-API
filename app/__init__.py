from flask import Flask, Blueprint
from .api.v1.routes import version_one as v1
from .api.v2.routes2 import version_two as v2
from flask_jwt_extended import JWTManager
from db_config import create_tables, create_super_admin


def create_app(config_name):
    app = Flask(__name__)
    create_tables()
    create_super_admin()

    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = "DFGHJ4657896578"

    app.url_map.strict_slashes = False

    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
