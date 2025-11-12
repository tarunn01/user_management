import hashlib, uuid
from datetime import datetime, timedelta
from app.models import User, Session, PasswordResetToken, LoginHistory
from app.database import SessionLocal


class UserManager:
    def __init__(self):
        self.db = SessionLocal()
        self.roles_permissions = {
            "admin": ["delete_user", "view_profile", "manage_roles"],
            "user": ["view_profile"],
            "guest": []
        }

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


    def register(self, username, email, password, role="user"):
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError("Username exists")

        user = User(
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
        if not user or user.password_hash != self._hash_password(password):
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