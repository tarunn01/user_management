import hashlib, uuid
from datetime import datetime, timedelta
from app.models import User, Session, PasswordResetToken, LoginHistory
from app.database import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    def __init__(self,db):
        self.db = db
        self.roles_permissions = {
            "admin": ["delete_user", "view_profile", "manage_roles"],
            "user": ["view_profile"],
            "guest": []
        }

    def _hash_password(self, password):
        return generate_password_hash(password,method = "pbkdf2:sha256",salt_length=16)

    def _verify_password(self, plain_password, stored_hash):
        """
        Verify a plaintext password against a stored password hash.

        Args:
            plain_password (str): The candidate plaintext password provided by the user.
            stored_hash (str): The hashed password stored in the database (from User.password_hash).

        Returns:
            bool: True if the candidate password matches the stored hash, False otherwise.

        Implementation note: This calls Werkzeug's `check_password_hash(stored_hash, candidate)`
        which internally handles the salt and PBKDF2 parameters encoded in the stored hash.
        Do NOT attempt to re-hash the candidate password and compare strings — that will fail
        because the hashing function generates a new salt each time.
        """
        if not stored_hash or not plain_password:
            return False
        return check_password_hash(stored_hash, plain_password)

    def register(self,firstname,lastname,username, email, password, role="user"):
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError("Username exists")

        user = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            role=role
        )
        self.db.add(user)
        self.db.commit()
        return user
    
    def login(self, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        # Use _verify_password to check the provided plaintext password against the stored hash.
        if not user or not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)
        session = Session(token=token, username=username, expires_at=expires_at)
        history = LoginHistory(id=str(uuid.uuid4()), username=username)

        self.db.add_all([session, history])
        self.db.commit()
        return session
    
    def has_permission(self, session_token, action):
        session = self.db.query(Session).filter_by(token=session_token).first()
        if not session or session.expires_at < datetime.utcnow():
            return False

        user = self.db.query(User).filter_by(username=session.username).first()
        if not user:
            return False

        permissions = self.roles_permissions.get(user.role, [])
        return action in permissions
    
    def request_password_reset(self, email):
        user = self.db.query(User).filter_by(email=email).first()
        if not user:
            raise ValueError("Email not found")

        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        reset = PasswordResetToken(token=token, username=user.username, expires_at=expires_at)

        self.db.add(reset)
        self.db.commit()
        return token
    
    def reset_password(self, token, new_password):
        reset = self.db.query(PasswordResetToken).filter_by(token=token).first()
        if not reset or reset.expires_at < datetime.utcnow():
            raise ValueError("Invalid or expired token")

        user = self.db.query(User).filter_by(username=reset.username).first()
        user.password_hash = self._hash_password(new_password)

        self.db.delete(reset)
        self.db.commit()