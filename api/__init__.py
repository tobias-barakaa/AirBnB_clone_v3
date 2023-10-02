from flask import Blueprint

"""
Create a Blueprint with the URL prefix "/api/v1"
"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views from your index.py
from . import index
