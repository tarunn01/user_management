# In app.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file before anything else
# We explicitly look for the .env file in the current directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    print(f"Loading .env from {dotenv_path}")
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found!")

# Import all models to ensure they are registered with SQLAlchemy
import models

from init import create_app
from extensions import db

# Create the Flask app instance using the factory
app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')