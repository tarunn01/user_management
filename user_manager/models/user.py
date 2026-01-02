# In models/user.py
from sqlalchemy import Column, String, DateTime
from extensions import db # Import db from the new extensions module
from datetime import datetime, timezone
import uuid

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = Column(String,nullable=False)
    lastname = Column(String,nullable=False)
    username = Column(String,nullable =False,unique=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(db.String(128), nullable=False)
    role = Column(db.String(128), default="user",nullable =False)
    # uuid: Unique identifier for external API references (separate from username login)
    uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # created_at: Timestamp when user account was created (UTC timezone-aware)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    # updated_at: Timestamp when user account was last modified (UTC timezone-aware)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
