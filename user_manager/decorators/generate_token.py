# In decorators/generate_token.py
from functools import wraps
import jwt
from flask import request, current_app
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in the 'Authorization' header
        if 'Authorization' in request.headers:
            # Expected format: "Bearer <token>"
            parts = request.headers['Authorization'].split()
            if len(parts) == 2:
                token = parts[1]

        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            # Decode the token using the correct secret key
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(uuid=data['user_id']).first()
            if not current_user:
                 return {'message': 'Token is invalid! User not found.'}, 401
        except Exception as e:
            return {'message': 'Token is invalid!', 'error': str(e)}, 401
        
        # Pass the user object to the decorated function as a keyword argument
        # This avoids issues with 'self' in class methods
        return f(*args, current_user=current_user, **kwargs)

    return decorated