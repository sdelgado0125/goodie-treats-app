import os
import csv
from functools import wraps
from flask import Flask, render_template, request, redirect, session, flash, g, jsonify
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from models import connect_db, db, User, Pet, Product, Recipe, Review, Follow, FavoriteRecipe, Brand
from csv import DictReader 
from api.brands_api import get_brands, add_brand
from api import api


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///goodie_treats')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DEV_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'  

bcrypt = Bcrypt(app)

connect_db(app)

app.register_blueprint(api)

@app.route('/api/brands', methods=['GET'])
def brands():
    """Fetch all pet food brands"""
    brands = get_brands()
    return jsonify([brand.to_dict() for brand in brands])

@app.route('/api/brands/<int:brand_id>', methods=['GET'])
def brand(brand_id):
    """Fetch a specific pet food brand by ID"""
    brand = add_brand(brand_id)
    if brand:
        return jsonify(brand.to_dict())
    else:
        return jsonify({"error": "Brand not found"}), 404

@app.before_request
def load_logged_in_user():
    """Loads the user if already signed in."""
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None

@app.before_request
def load_logged_in_user():
    """Loads the user if already signed in."""
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None

def login_required(f):
    """Requires user to login before accessing page."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first.", "warning")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def root():
    return redirect("/homepage")

@app.route('/homepage')
@login_required
def home():
    """Homepage."""
    return render_template('base.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles User login"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Welcome back!", "success")
            return redirect("/homepage")
        else:
            flash("Invalid username or password.", "danger")  # This flashes an error message

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if not g.user:
        return redirect('/login') 
    

    recipes_count = Recipe.query.filter_by(user_id=g.user.id).count()
    products_count = Product.query.count() 
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(5).all() 
    
    return render_template(
        'dashboard.html', 
        username=g.user.username, 
        recipes_count=recipes_count, 
        products_count=products_count, 
        featured_products=featured_products
    )


@app.route('/logout')
def logout():
    """Handles Loging out the user"""
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register User"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Choose another.", "danger")
            return redirect('/register')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists. Choose another.", "danger")
            return redirect('/register')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()


        session['user_id'] = new_user.id

        flash("Registration successful! Welcome!", "success")
        return redirect('/user_info')  # Redirect to the /user_info route

    return render_template('register.html')



@app.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    """Handle user profile and pet information update."""
    if request.method == 'POST':
    
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        image = request.files.get('image')

        if not first_name or not last_name:
            flash("First name and last name are required.", "danger")
            return redirect('/user_info')

        image_path = ''
        if image:
            filename = secure_filename(image.filename)
            if filename: 
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    image.save(image_path)
                except Exception as e:
                    flash(f"Image upload failed: {e}", "danger")
                    return redirect('/user_info')

        user = User.query.get(session['user_id'])
        user.first_name = first_name
        user.last_name = last_name
        user.image = image_path if image_path else user.image 

        pet_type = request.form['pet_type'].strip()
        name = request.form['name'].strip()
        breed = request.form['breed'].strip()
        age = request.form.get('age', type=int)
        weight = request.form.get('weight', type=float)

        if Pet.query.filter_by(user_id=user.id, name=name, pet_type=pet_type).first():
            flash("A pet with the same name and type already exists.", "danger")
            return redirect('/user_info')

        new_pet = Pet(
            user_id=user.id,
            pet_type=pet_type,
            name=name,
            breed=breed,
            age=age,
            weight=weight
        )
        db.session.add(new_pet)

        try:
            db.session.commit()
            flash("Profile and pet information updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {e}", "danger")

        return redirect('/')

    return render_template('user_info.html')

@app.route('/profile')
def profile():
    """Display user's profile information."""
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your profile.", "danger")
        return redirect('/login')
    
    # Query the user information from the database
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect('/')

    # Query any pets associated with the user
    pets = Pet.query.filter_by(user_id=user_id).all()

    return render_template('profile.html', user=user, pets=pets)





@app.route('/products')
def product():
    brands = Brand.query.all()  # Retrieve all brands from the database
    return render_template('products.html', brands=brands)

@app.route('/recipes')
def recipes():
    """Displays the recipes page, requires login."""
    if 'user_id' not in session:
        flash("You must be logged in to view this page.", "danger")
        return redirect("/login")
    
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    """Render the create recipe form and handle form submission."""
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        
        if title and ingredients and instructions:
            new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=g.user.id)
            db.session.add(new_recipe)
            db.session.commit()
            flash("Recipe created successfully!", "success")
            return redirect('/recipes')
        
        flash("All fields are required!", "danger")
    
    return render_template('create_recipe.html')

@app.route('/favorite_recipe')
def favorite_recipe():
    """Render user's favorite recipes."""
    favorite_recipes = g.user.favorite_recipes
    return render_template('favorite_recipe.html', recipes=favorite_recipes)


@app.context_processor
def inject_user():
    return {'user': g.user}

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)