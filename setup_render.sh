#!/bin/bash

# Step 1: Create and activate virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate || { echo "Failed to activate virtual environment. Exiting."; exit 1; }

# Step 2: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt || { echo "Failed to install dependencies. Exiting."; exit 1; }

# Step 3: Set up environment variables
read -p "Enter your DATABASE_URL (e.g., postgresql://username:password@localhost/goodie_treats): " DATABASE_URL
export DATABASE_URL="$DATABASE_URL"
echo "DATABASE_URL has been set."

# Step 4: Initialize the database
echo "Initializing the database..."
python3 -c "
from app import db
db.create_all()
print('Database initialized successfully!')
" || { echo "Database initialization failed. Exiting."; exit 1; }

# Step 5: Final instructions
echo ""
echo "Setup is complete!"
echo "To run the application, use the following commands:"
echo "source venv/bin/activate"
echo "flask run"
echo ""
echo "If deploying on Render, ensure your environment variables are set in the Render dashboard."
