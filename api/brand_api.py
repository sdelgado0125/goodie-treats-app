from flask import Blueprint, jsonify, request
from models import db, Brand

brand_bp = Blueprint('brand_api', __name__)

@brand_bp.route('/brands', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    return jsonify([brand.to_dict() for brand in brands])

@brand_bp.route('/brands', methods=['POST'])
def add_brand():
    data = request.get_json()
    new_brand = Brand(name=data['name'], description=data.get('description', ''))
    db.session.add(new_brand)
    db.session.commit()
    return jsonify(new_brand.to_dict()), 201