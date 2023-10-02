#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
"""
running first app
"""
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
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run the Flask application with the specified host and port
    app.run(host=host, port=port)
