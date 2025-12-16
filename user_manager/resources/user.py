# In resources/user.py
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from decorators.generate_token import token_required
from models.user import User
from init import db,bcrypt
from serializers.user import UserSchema

user_schema =UserSchema()
users_schema = UserSchema(many=True)

class UserResource(Resource):
    @token_required
    def get(self, current_user):
        users = User.query.all()
        # This is a temporary, simple way to return users
        return users_schema.dump(users)

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'no input data provided'},400
        try:
            # Don't load into a User object yet, just validate the data
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # Now, create the User object
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data['username'],
            email=data['email'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created', 'user': user_schema.dump(new_user)}, 201
