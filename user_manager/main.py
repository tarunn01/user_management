from flask import Flask
from flask_restful import Api
from app.api import RegisterResource, LoginResource, UsersResource
from app.database import Base, engine

from app.database import Base, engine
from app import models


Base.metadata.create_all(engine)

def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(RegisterResource, "/api/users/register")
    api.add_resource(LoginResource, "/api/users/login")
    api.add_resource(UsersResource, "/api/users")

    return app


if __name__ == "__main__":
# Create tables in dev if not present
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)