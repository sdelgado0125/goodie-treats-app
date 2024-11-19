import os
from csv import DictReader
from app import app, db  
from models import Brand 

with app.app_context():
    with open("csvs/brand.csv", "r") as file:
        csv_reader = DictReader(file)

        for row in csv_reader:
            brand = Brand(
                name=row['name'],
                description=row['description']
            )

            db.session.add(brand)

        db.session.commit()

    print("Brands have been successfully populated into the database.")
