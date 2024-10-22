import os

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/')
def root():
    return redirect("/homepage")

@app.route('/homepage')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/products')
def product():
    return render_template('products.html')


if __name__ == '__main__':
    app.run(debug=True)

