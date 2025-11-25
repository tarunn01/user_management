from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime, timezone
import uuid

class User(Base):
    __tablename__ = "users"
    Firstname = Column(String,nullable=False)
    Lastname = Column(String,nullable=False)
    username = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    # uuid: Unique identifier for external API references (separate from username login)
    uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # created_at: Timestamp when user account was created (UTC timezone-aware)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    # updated_at: Timestamp when user account was last modified (UTC timezone-aware)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Session(Base):
    __tablename__ = "sessions"
    token = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    expires_at = Column(DateTime, nullable=False)

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    token = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    expires_at = Column(DateTime, nullable=False)

class LoginHistory(Base):
    __tablename__ = "login_history"
    id = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    # timestamp: When the login occurred (UTC timezone-aware)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)