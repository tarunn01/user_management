import jwt
import datetime
from flask import request, current_app
from flask_restful import Resource
from models.user import User
from init import db, bcrypt

class LoginResource(Resource):
    def post(self):
        """
        POST /api/users/login
        Public endpoint (no auth required) to log in a user."""
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        #check if the user exists or password is correct.
        if user and bcrypt.check_password_hash(user.password_hash,data.get('password')):
            #generate JWT token
            jwt_token = jwt.encode({
                'user_id' :user.uuid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },current_app.config['JWT_SECRET_KEY'])
            return {'token': jwt_token}, 200
        else:
            return {'message': 'Invalid username or password'},401