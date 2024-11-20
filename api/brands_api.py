import os
from flask import request, jsonify
from . import api
from models import Brand, Product, db
import csv

@api.route('/brands', methods=['GET'])
def get_brands():
    """Fetch all brands from the CSV file."""
    brands = []
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'csvs', 'brand.csv')  # Adjust path as needed
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Validate and sanitize data
                try:
                    row['id'] = int(row['id']) if row['id'] else None
                    row['name'] = row['name'].strip() if row['name'] else "Unknown"
                    row['description'] = row['description'].strip() if row['description'] else "No description available"
                    brands.append(row)
                except Exception as e:
                    print(f"Skipping invalid row: {row}, Error: {e}")
        return jsonify(brands)  # Return the valid brands as JSON
    except FileNotFoundError:
        return jsonify({'error': 'brand.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# POST route to add a new brand
@api.route('/brands', methods=['POST'])
def add_brand():
    """Add a new brand to the database."""
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'description', 'rating']):
        return jsonify({'error': 'Invalid input'}), 400

    try:
        new_brand = Brand(
            name=data['name'],
            description=data['description'],
            rating=data['rating']
        )
        db.session.add(new_brand)
        db.session.commit()
        return jsonify({'message': 'Brand added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/products', methods=['GET'])
def get_products():
    """Fetch all products from the database."""
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'brand_id': product.brand_id,
        'rating': product.rating,
        'healthiness': product.healthiness,
        'ingredients': product.ingredients
    } for product in products])