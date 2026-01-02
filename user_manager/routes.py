# In routes.py
from flask import Blueprint
from flask_restful import Api
from resources.rule import RuleResource
from resources.user import UserResource
from resources.login import LoginResource
from resources.health import Health
from resources.enrollment import EnrollmentResource
# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Add resources to the API
api.add_resource(UserResource, '/users')
api.add_resource(LoginResource, '/login')
api.add_resource(Health, '/health')
api.add_resource(RuleResource, '/rules')
api.add_resource(EnrollmentResource,'/enrollment/<string:action>')