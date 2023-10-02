#!/usr/bin/python3
"""
script to running the first app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exception):
    """
    This function is called when the Flask app context is torn down.

    Args:
        exception (Exception): The exception, if any, that triggered the teardown.

    Returns:
        None
    """
    storage.close()

if __name__ == "__main__":
    # Get the host and port values from environment variables or use defaults
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
