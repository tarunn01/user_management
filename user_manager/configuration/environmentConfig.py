# In configuration/environmentConfig.py
import os

class Config:
    """
    Base configuration class.
    Reads environment variables.
    """
    DATABASE_URI = os.getenv('DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')