from flask import Flask
from models import storage  # Import the storage module correctly
from api.v1.views import app_views  # Import app_views correctly

app = Flask(__name__)

# Register the app_views blueprint with the Flask application
app.register_blueprint(app_views)

# Define a function to be called when the app context is torn down
@app.teardown_appcontext
def close_storage(exception):
    """
    This function is called when the Flask app context is torn down.

    Args:
        exception (Exception): The exception, if any, that triggered the teardown.

    Returns:
        None
    """
    # Close the storage connection to release resources
    storage.close()

if __name__ == "__main__":
    # Run the Flask application when the script is executed
    app.run()
