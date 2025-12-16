# In configuration/environmentConfig.py
import os
from dotenv import load_dotenv

# This line loads the variables from .env into the environment
load_dotenv()

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

# You could add other classes like ProdConfig or TestConfig here later
# For now, we'll just have a function to load the dev config.

def load_env_configs():
    return DevConfig()