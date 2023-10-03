#!/usr/bin/python3
"""
script to running the first app
"""

from flask import Flask, make_response, jsonify
from models import storage
from flasgger import Swagger
from os import getenv
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """
    This function is called when the Flask app context is torn down.

    Args:
        exception (Exception): The exception,
        if any, that triggered the teardown.

    Returns:
        None
    """
    storage.close()


# Define a handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    # Get the host and port values from environment variables or use defaults
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
