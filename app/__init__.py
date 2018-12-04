
from flask import Flask, Blueprint
from .api.v1.routes import version_one as v1
from flask_jwt_extended import JWTManager

def create_app(config_name):
    app = Flask(__name__)
    app.url_map.strict_slashes = False    
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = "DFGHJ4657896578"
    app.register_blueprint(v1)
    return app

    