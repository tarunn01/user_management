from sqlalchemy import Column, String, DateTime, ForeignKey
from init import db
from datetime import datetime, timezone
import uuid

class User(db.Model):
    __tablename__ = "users"
    firstname = Column(String,nullable=False)
    lastname = Column(String,nullable=False)
    username = Column(String, primary_key=True,nullable =False,unique=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(db.String(128), nullable=True)
    role = Column(db.String(128), default="user",nullable =False)
    # uuid: Unique identifier for external API references (separate from username login)
    uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # created_at: Timestamp when user account was created (UTC timezone-aware)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    # updated_at: Timestamp when user account was last modified (UTC timezone-aware)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Session(db.Model):
    __tablename__ = "sessions"
    token = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    expires_at = Column(DateTime, nullable=False)

class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"
    token = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    expires_at = Column(DateTime, nullable=False)

class LoginHistory(db.Model):
    __tablename__ = "login_history"
    id = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    # timestamp: When the login occurred (UTC timezone-aware)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)