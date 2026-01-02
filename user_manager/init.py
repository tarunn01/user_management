# In init.py
from flask import Flask, jsonify
from configuration.environmentConfig import Config
from extensions import db, bcrypt, ma, cache
from routes import api_bp

def create_app():
    """Application Factory"""
    
    # Validate configuration
    if not Config.DATABASE_URI or not Config.JWT_SECRET_KEY:
        raise RuntimeError("DATABASE_URI and JWT_SECRET_KEY must be set in the environment")

    # DEBUG PRINT
    print(f"DEBUG: Config.REDIS_URL is: {Config.REDIS_URL}")

    app = Flask(__name__)
    
    # Configure the application using the Config object
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = Config.REDIS_URL

    # Associate extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    
    # Register the API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # Add a simple root route for health checks
    @app.route('/')
    def index():
        return jsonify({"message": "API is running"})

    return app