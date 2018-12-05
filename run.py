from flask import Flask, jsonify, make_response

from app import create_app

app = create_app(config_name="testing")


@app.errorhandler(404)
def page_not_found(e):
    """error handler default method for error 404"""

    return make_response(
        jsonify(
            {"message": "Oops! not found, check you have \
            right url or correct input type", "status": 404}
            ), 404
        )


@app.route('/')
def landing_page():
    """method for default message on landing page"""

    return "Welcome to Eric iReporter"


if __name__ == '__main__':
    app.run(debug=True)
