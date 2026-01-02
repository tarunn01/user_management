# In services/user_service.py
from models.user import User
from extensions import db, bcrypt
import jwt
import datetime
from flask import current_app

class UserService:

    def get_all_users(self):
        return User.query.all()

    def create_user(self, data):
        """
        Handles the business logic of creating a new user.
        Expects 'data' to be a dictionary.
        """
        # Check if user already exists
        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return None

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
        
        return new_user

    def login_user(self, username, password):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            jwt_token = jwt.encode({
                'user_id': user.uuid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
            return jwt_token
        
        return None