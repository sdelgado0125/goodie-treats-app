from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150)) 
    last_name = db.Column(db.String(150))
    image = db.Column(db.String(150))  
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    favorite_recipes = db.relationship('Recipe', secondary='favorite_recipe', back_populates='favorited_by')

    followers = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower_user', lazy='dynamic', overlaps="follower")
    following = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic', overlaps="followed")
class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    breed = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    
class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
    
class Product(db.Model):
    __tablename__= 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    healthiness = db.Column(db.String(50), nullable = False)
    ingredients = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    brand = db.relationship('Brand', backref='products')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand_id": self.brand_id,
            "rating": self.rating,
            "healthiness": self.healthiness,
            "ingredients": self.ingredients,
            "created_at": self.created_at
        }


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    favorited_by = db.relationship('User', secondary='favorite_recipe', back_populates='favorite_recipes')
    
class FavoriteRecipe(db.Model):
    __tablename__ = 'favorite_recipe'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class Review(db.Model):
    __tablename__= 'review'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='reviews')

class Follow(db.Model):
    __tablename__= 'follow'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    follower = db.relationship('User', foreign_keys=[follower_id], overlaps="followers")
    followed = db.relationship('User', foreign_keys=[followed_id], overlaps="following")
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)