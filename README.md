# Goodie Treats

Goodie Treats is a web-based platform that helps pet owners find the best food products for their pets. Users can search for products, see ratings, and save their favorite recipes. The platform offers the ability to create and share pet-friendly recipes, as well as review and rate different brands and products.

This project was created using Flask, SQLAlchemy, and Python and is hosted on Render.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Instructions](#installation-instructions)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User Authentication:** Users can register, log in, and manage their profiles.
- **Create and Share Recipes:** Users can create pet-friendly recipes and share them with others.
- **Favorite Recipes:** Users can mark recipes as favorites and view them later.
- **Product Ratings:** Users can rate pet food products and see others’ reviews.
- **Admin Panel:** Admins can manage the content (e.g., products, recipes).
- **Responsive Design:** The app works seamlessly on mobile devices and desktops.

---

## Tech Stack

This project was built using the following technologies:

- **Flask:** A micro web framework for Python.
- **SQLAlchemy:** A powerful ORM for database management.
- **SQLite/PostgreSQL:** Database for storing user, recipe, and product information.
- **HTML5, CSS3, JavaScript:** For frontend development.
- **Jinja2:** Templating engine for dynamic page rendering.
- **Flask-Bcrypt:** For secure password hashing.
- **Flask-Login:** For user authentication and session management.
- **Gunicorn:** WSGI HTTP Server for serving the app in production.

---

## Installation Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sdelgado0125/goodie-treats.git
   cd goodie-treats
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**

```bash
Set the DATABASE_URL environment variable to configure the database connection. For example:

export DATABASE_URL='postgresql://username:password@localhost/goodie_treats'

Replace username, password, and localhost/goodie_treats with your actual database details.
```

5. **Initialize the Database**


Run the following commands to create the tables if they don’t already exist:
```bash
from app import db
db.create_all()
```
Alternatively, you can add a route to your app for database initialization:
```bash
@app.route('/initialize-db')
def initialize_db():
    db.create_all()
    return "Database initialized successfully!"
```
Navigate to http://127.0.0.1:5000/initialize-db in your browser to trigger this function.

6. **Run the App**

```bash
flask run
```

## Project Schema

Schema Diagram

Below is a visual representation of the relationships between the models in the project:
	•	User: Has many recipes and reviews.
	•	Recipe: Belongs to a user and can have many users marking it as a favorite.
	•	Product: Can be rated by many users via reviews.
	•	Review: Belongs to a user and a product.

Schema Relationships

User
  ├── Recipe (One-to-Many)
  ├── FavoriteRecipe (Many-to-Many via favorites table)
  ├── Review (One-to-Many)

Recipe
  ├── User (Many-to-One)

Product
  ├── Review (One-to-Many)

Review
  ├── User (Many-to-One)
  ├── Product (Many-to-One)

Here’s the models.py showing the relationships:

```bash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    recipes = db.relationship('Recipe', backref='user')
    reviews = db.relationship('Review', backref='user')
    favorites = db.relationship('Recipe', secondary='favorites', backref='favorited_by')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    reviews = db.relationship('Review', backref='product')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
```
Contributing

Contributing
We welcome contributions to Goodie Treats! If you’d like to improve the app or fix a bug, please follow these steps:

Fork the repository
Create your own copy of the repository by forking it.

Clone the forked repository

```bash
git clone https://github.com/your-username/goodie-treats.git
cd goodie-treats
```

Create a new branch for your changes


```bash
git checkout -b <feature-name>
Replace feature-name with a short, descriptive name for your changes.
```

Make your changes
Modify the codebase to fix the issue or add your feature.

Commit your changes

```bash
git commit -am 'Your commit message'
Push to your fork
```

```bash
git push origin feature-name
Create a pull request
Open a pull request from your fork’s branch to the main repository. Provide a clear description of your changes.
```

Respond to feedback
Be available to discuss and address any feedback from the project maintainer.
