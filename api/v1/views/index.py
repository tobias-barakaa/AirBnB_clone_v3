from . import app_views  # Import the app_views Blueprint

@app_views.route('/status', methods=['GET'])
def get_status():
    """
    This function defines a route that returns a JSON response with the status "OK".

    Returns:
        JSON response with the status "OK"
    """
    return {"status": "OK"}, 200
