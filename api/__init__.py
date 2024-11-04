from flask import Flask
from api.brand_api import brand_bp

def create_api(app):
    app.register_blueprint(brand_bp, url_prefix='/api')