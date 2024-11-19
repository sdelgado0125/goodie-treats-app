from csv import DictReader
from models import db, Brand

# Drop the 'Brand' table
Brand.__table__.drop(db.engine)

# Recreate the 'Brand' table
Brand.__table__.create(db.engine)

# Open and read the CSV file
with open("csvs/brand.csv", "r") as file:
    csv_reader = DictReader(file)
    
    # Iterate over each row in the CSV
    for row in csv_reader:
        # Create a new Brand instance for each row
        brand = Brand(
            id=row['id'],  # Assuming 'id' is a column in your CSV
            name=row['name'],
            description=row['description']
        )
        
        # Add the brand to the session
        db.session.add(brand)

# Commit the session to save all records to the database
db.session.commit()
print("Data has been successfully added to the database.")

