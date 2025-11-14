from flask import Flask
from flask_restful import Api
import os
from datetime import timedelta
from dotenv import load_dotenv
from app.api import RegisterResource, LoginResource, UsersResource
from app.database import Base, engine

from app.database import Base, engine
from app import models


Base.metadata.create_all(engine)

def create_app():
    load_dotenv()  # Load environment variables from .env file
    app = Flask(__name__)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY",
        "JWT_SECRET_KEY"  # fallback only for local/dev; replace in prod
    )
    # use env var in prod
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)

    api.add_resource(RegisterResource, "/api/users/register")
    api.add_resource(LoginResource, "/api/users/login")
    api.add_resource(UsersResource, "/api/users")

    return app


if __name__ == "__main__":
# Create tables in dev if not present
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)