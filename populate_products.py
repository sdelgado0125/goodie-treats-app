import os
from csv import DictReader
from app import app, db
from models import Product

with app.app_context():
    with open("csvs/product.csv", "r") as file:
        csv_reader = DictReader(file)

        for row in csv_reader:
            product = Product(
                name=row['name'],
                brand_id=row['brand_id'],  # Ensure this matches a valid brand ID
                rating=row['rating'],
                healthiness=row['healthiness'],
                ingredients=row['ingredients']
            )

            db.session.add(product)

        db.session.commit()

    print("Products have been successfully populated into the database.")
