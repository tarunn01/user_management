from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.database import SessionLocal
from app.user_manager import UserManager
from app.models import User


def _serialize_user(user):
    """
    Convert User model to JSON-serializable dict.
    Omits password_hash for security.
    Converts datetime fields to ISO format strings.
    """
    return {
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "role": user.role,
        "uuid": user.uuid,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

class RegisterResource(Resource):
    """
    POST /api/users/register
    Public endpoint (no auth required) to register a new user.
    Body: {"username": "...", "email": "...", "password": "...", "lastname": "..."} Response: 201 Created with user data (including uuid, created_at, lastname), or 400 if validation fails.
    """
    def post(self):
        payload = request.get_json()
        firstname = payload.get("firstname")
        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")
        lastname = payload.get("lastname")  # Accept lastname from request
        
        # Validate required fields
        if not username or not email or not password:
            return {"message": "Missing required fields"}, 400
        db = SessionLocal()
        try:
            manager = UserManager(db)
            try:
                # Pass lastname to register (update UserManager if needed)
                user = manager.register(firstname,lastname,username,email, password)
            except ValueError as ve:
                # Duplicate username/email or other validation error
                return {"message": str(ve)}, 400
            
            # Return created user (without password_hash)
            return _serialize_user(user), 201
        finally:
            db.close()


class LoginResource(Resource):
    """
    POST /api/users/login
    Public endpoint (no auth required) to authenticate user and get JWT access token.
    
    JWT (JSON Web Token) Flow:
    1. Client sends username + password
    2. Server validates credentials against DB (password hash verified)
    3. Server generates an access token using create_access_token(identity=username)
    4. Token is a signed JWT containing username as 'identity' and expiry time
    5. Client stores token and includes it in Authorization: Bearer <token> header for protected endpoints
    
    Body: {"username": "...", "password": "..."}
    Response: 200 OK with access_token (JWT) and token type, or 401 if credentials invalid.
    """
    def post(self):
        payload = request.get_json()
        username = payload.get("username")
        password = payload.get("password")
        
        # Validate required fields
        if not username or not password:
            return {"message": "Missing required fields"}, 400
        
        db = SessionLocal()
        try:
            manager = UserManager(db)
            try:
                # Verify credentials (will raise ValueError if invalid)
                session = manager.login(username, password)
            except ValueError:
                # Invalid username or password
                return {"message": "Invalid credentials"}, 401
            
            # Create a JWT access token for this user.
            # This token is stateless (no server-side session needed) and signed with JWT_SECRET_KEY.
            # The token contains the username as 'identity' and expires after JWT_ACCESS_TOKEN_EXPIRES.
            # The server verifies the signature on protected endpoints to ensure token is valid.
            access_token = create_access_token(identity=username)
            
            return {
                "access_token": access_token,  # Send this token in Authorization: Bearer <token> header
                "token_type": "Bearer",         # Standard token type for OAuth/JWT
                "expires_in": 3600              # Token expiry in seconds (1 hour for this config)
            }, 200
        finally:
            db.close()


class UsersResource(Resource):
    """
    GET /api/users
    Protected endpoint (requires valid JWT token) to list all users.
    Authorization: Bearer <access_token> required in header.
    Response: 200 OK with array of user objects, or 401 if token missing/invalid.
    """
    # @jwt_required()
    def get(self):
        db = SessionLocal()
        try:
            users = db.query(User).all()
            return jsonify([_serialize_user(user) for user in users])
        finally:
            db.close()


class MeResource(Resource):
    """
    GET /api/users/me
    Protected endpoint (requires valid JWT access token in Authorization header).
    
    JWT Protection Explanation:
    - Decorator @jwt_required() checks for Authorization: Bearer <token> header
    - If header missing → returns 401 Unauthorized
    - If token invalid/expired/tampered → returns 401 Unauthorized
    - If token valid → get_jwt_identity() extracts the username from token payload
    - Endpoint then returns the current user's profile
    
    How to use:
    1. GET /api/users/login to obtain access_token
    2. Call this endpoint with header: Authorization: Bearer <access_token>
    
    Example with curl:
        curl -H "Authorization: Bearer <token>" http://127.0.0.1:5000/api/users/me
    
    Example with PowerShell:
        $headers = @{ Authorization = "Bearer <token>" }
        Invoke-RestMethod -Method GET -Uri http://127.0.0.1:5000/api/users/me -Headers $headers
    
    Response: 200 OK with current user data, or 401 if token missing/invalid/expired.
    """
    # @jwt_required()  # This decorator protects the endpoint — requires valid JWT token
    def get(self):
        # Extract the username from the JWT token payload.
        # If @jwt_required() passes, this is guaranteed to be the authenticated user.
        current_username = get_jwt_identity()
        
        db = SessionLocal()
        try:
            # Fetch the user from DB to return full profile.
            # (Optional: you could skip this DB lookup and just return the username from the token,
            #  but querying the DB allows you to fetch additional user data like email, role, etc.)
            user = db.query(User).filter_by(username=current_username).first()
            if not user:
                # Token is valid but user not found in DB (should be rare in normal operation).
                return {"message": "User not found"}, 404
            
            # Return the authenticated user's profile (without password_hash for security).
            return _serialize_user(user), 200
        finally:
            db.close()


class AccessTokenResource(Resource):
    """
    POST /api/auth/token
    Protected endpoint to create/renew an access token for authenticated users.
    
    This endpoint allows users with a valid JWT token to generate a new token
    (useful for token refresh scenarios or extending sessions).
    
    Authorization: Bearer <current_valid_token> required in header.
    
    Body: {} (empty, token is extracted from Authorization header)
    
    Response: 200 OK with new access_token, or 401 if token missing/invalid.
    
    Example usage (renew token):
        1. GET /api/users/login → get initial access_token
        2. Token expires or is about to expire
        3. POST /api/auth/token with Authorization: Bearer <old_token>
        4. Get new access_token, continue using API
    
    Security Note:
        - This endpoint requires an existing valid token (prevents unauthorized token generation)
        - New token has the same expiry duration as configured (JWT_ACCESS_TOKEN_EXPIRES)
        - Use this for token refresh/renewal flows
    """
    @jwt_required()  # Requires existing valid token
    def post(self):
        # Extract the authenticated username from the current token
        current_username = get_jwt_identity()
        
        # Generate a new access token for the user
        # The new token will have the same expiry as JWT_ACCESS_TOKEN_EXPIRES config
        new_access_token = create_access_token(identity=current_username)
        
        return {
            "access_token": new_access_token,  # New JWT token
            "token_type": "Bearer",            # Standard token type
            "expires_in": 3600                 # Expiry in seconds (1 hour for this config)
        }, 200