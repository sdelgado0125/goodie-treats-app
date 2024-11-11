from flask import request, jsonify
from . import api
from models import Brand, db 

# GET route to fetch all pet food brands
@api.route('/brands', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    brand_list = []
    for brand in brands:
        brand_list.append({
            'id': brand.id,
            'name': brand.name,
            'description': brand.description,
            'rating': brand.rating
        })
    return jsonify(brand_list), 200


@api.route('/brands', methods=['POST'])
def add_brand():
    data = request.get_json()
    new_brand = Brand(
        name=data['name'],
        description=data['description'],
        rating=data['rating']
    )
    db.session.add(new_brand)
    db.session.commit()
    return jsonify({'message': 'Brand added successfully'}), 201


