from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from configuration.environmentConfig import load_env_configs

app = Flask(__name__)
api = Api(app)

# Configure the application using the Config object
app.config.from_object(load_env_configs())

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Import resources to register the routes
from resources.user import UserResource
from resources.login import LoginResource
from resources.health import Health

# Add a simple root route for health checks
@app.route('/')
def index():
    return jsonify({"message": "API is running"})

# Register API resources
api.add_resource(UserResource, '/users')
api.add_resource(LoginResource, '/login')
api.add_resource(Health, '/health')
