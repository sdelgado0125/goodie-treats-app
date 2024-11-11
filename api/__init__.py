from flask import Blueprint

# Initialize the blueprint for API
api = Blueprint('api', __name__, url_prefix='/api')

# Import the routes from brands_api.py
from .brands_api import *
