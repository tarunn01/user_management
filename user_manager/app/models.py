from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")

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
    timestamp = Column(DateTime, default=datetime.utcnow)