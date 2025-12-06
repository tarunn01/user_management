# In resources/user.py
from flask_restful import Resource
from flask import request
from models.user import User
from init import db

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        # This is a temporary, simple way to return users
        return [{'id': user.id, 'username': user.username} for user in users]

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 201
