from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from dotenv import load_dotenv
from app.api import RegisterResource, LoginResource, UsersResource, MeResource, AccessTokenResource
from app.database import Base, engine
from app import models


Base.metadata.create_all(engine)

def create_app():
    load_dotenv()  # Load environment variables from .env file
    app = Flask(__name__)
    api = Api(app)
    
    # =========================================
    # JWT Configuration (MUST be before JWTManager initialization)
    # =========================================
    # The secret key used to sign and verify JWT tokens.
    # IMPORTANT: In production, always use a strong secret from environment variables or secrets manager.
    # Example: export JWT_SECRET_KEY="<strong-random-secret>" before running the app.
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY",
        "dev-only-change-in-production"  # fallback only for local/dev; replace in prod
    )
    
    # How long JWT access tokens are valid (in minutes).
    # Keep this reasonably short (15min-1hr) for security.
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    
    # Initialize JWTManager AFTER setting config.
    # This enables @jwt_required() decorator and token creation/verification functions.
    jwt = JWTManager(app)
    
    # =========================================
    # Register API Resources (endpoints)
    # =========================================
    # Public endpoints (no JWT required)
    api.add_resource(RegisterResource, "/api/users/register")
    api.add_resource(LoginResource, "/api/users/login")
    
    # Protected endpoints (JWT required in Authorization header)
    api.add_resource(UsersResource, "/api/users")
    api.add_resource(MeResource, "/api/users/me")
    api.add_resource(AccessTokenResource, "/api/auth/token")  # Token creation/renewal endpoint
    
    return app

if __name__ == "__main__":
# Create tables in dev if not present
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)