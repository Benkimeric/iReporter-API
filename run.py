from flask import Flask, jsonify, make_response

from app import create_app

app = create_app(config_name="testing")


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
    return make_response(
        jsonify(
            {
                "message": "iReporter Server error. Please contact the admin",
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


if __name__ == '__main__':
    app.run(debug=True)
