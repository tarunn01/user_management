# In resources/login.py
from flask import request
from flask_restful import Resource
from services.user_service import UserService

user_service = UserService()

class LoginResource(Resource):
    def post(self):
        """Handles POST request for user login."""
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return {'message': 'Username and password are required'}, 400

        username = data.get('username')
        password = data.get('password')

        # Use the service to handle the login logic
        token = user_service.login_user(username, password)

        if token:
            return {'token': token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401
