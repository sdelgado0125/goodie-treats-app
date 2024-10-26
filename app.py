import os
from functools import wraps
from flask import Flask, render_template, request, redirect, session, flash, g
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from models import connect_db, db, User, Pet, Product, Recipe, Review, Follow 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///goodie_treats')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DEV_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ensure 'uploads/' exists and is writable

bcrypt = Bcrypt(app)

connect_db(app)

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

    # This will render the login.html and include any flashed messages
    return render_template('login.html')

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
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    """Handle user profile and pet information update."""
    if request.method == 'POST':
    
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        image = request.files.get('image')

        # Validate user input
        if not first_name or not last_name:
            flash("First name and last name are required.", "danger")
            return redirect('/user_info')

        # Handle image upload
        image_path = ''
        if image:
            filename = secure_filename(image.filename)  # Sanitize filename
            if filename:  # Ensure file has a valid name
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    image.save(image_path)  # Save the image to the upload folder
                except Exception as e:
                    flash(f"Image upload failed: {e}", "danger")
                    return redirect('/user_info')

        # Update user information
        user = User.query.get(session['user_id'])
        user.first_name = first_name
        user.last_name = last_name
        user.image = image_path if image_path else user.image  # Keep the old image if no new one

        pet_type = request.form['pet_type'].strip()
        name = request.form['name'].strip()
        breed = request.form['breed'].strip()
        age = request.form.get('age', type=int)
        weight = request.form.get('weight', type=float)

        if Pet.query.filter_by(user_id=user.id, name=name, pet_type=pet_type).first():
            flash("A pet with the same name and type already exists.", "danger")
            return redirect('/user_info')

        # Add new pet information
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

        return redirect('/homepage')

    return render_template('user_info.html')


@app.route('/products')
def product():
    return render_template('products.html')

@app.route('/recipes')
def recipes():
    """Displays the recipes page, requires login."""
    if 'user_id' not in session:
        flash("You must be logged in to view this page.", "danger")
        return redirect("/login")
    
    # Fetch recipes from the database to display
    recipes = Recipe.query.all()  # Example: adjust based on your query
    return render_template('recipes.html', recipes=recipes)

@app.context_processor
def inject_user():
    return {'user': g.user}

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)