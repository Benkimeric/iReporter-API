from flask import Flask, Blueprint, make_response, jsonify
from .api.v1.routes import version_one as v1
from .api.v2.routes_v2 import version_two as v2
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

    @app.errorhandler(404)
    def page_not_found(e):
        """error handler default method for error 404"""

        return make_response(
            jsonify(
                {"message": "Oops! not found, check you have "
                 "right url or correct input type", "status": 404}
                ), 404
            )

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        print(e)
        return make_response(
            jsonify(
                {
                    "message": "iReporter Server error. "
                    "Please contact the admin",
                    "status": 500
                }
            ), 500
        )

    @app.route('/')
    def landing_page():
        """method for default message on landing page"""

        return make_response(
            jsonify(
                {
                    "message": "Welcome to Eric's iReporter App"
                }
            )
        )

    return app
