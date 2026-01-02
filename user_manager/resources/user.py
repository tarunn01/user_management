# In resources/user.py
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from decorators.generate_token import token_required
from serializers.user import UserSchema
from services.user_service import UserService

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_service = UserService()

class UserResource(Resource):
    @token_required
    def get(self, current_user):
        """Handles GET request to retrieve all users."""
        users = user_service.get_all_users()
        return users_schema.dump(users)

    def post(self):
        """Handles POST request to create a new user."""
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        
        try:
            # Validate the input data
            # We expect a dictionary now, not a User object
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # Use the service to create the user
        new_user = user_service.create_user(data)

        if new_user is None:
            return {'message': 'User with that username or email already exists'}, 409 # 409 Conflict

        return {'message': 'User created', 'user': user_schema.dump(new_user)}, 201