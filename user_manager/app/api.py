from flask import jsonify, request
from flask_restful import Resource
from app.database import SessionLocal
from app.user_manager import UserManager
from app.models import User


def _serialize_user(user):
    return{"username":user.username,
           "email":user.email,
           "role":user.role
           }

class RegisterResource(Resource):
    def post(self):
        payload =request.get_json()
        username =payload.get("username")
        email =payload.get("email")
        password =payload.get("password")
        if not username or not email or not password:
            return{"message":"Missing required fields"},400
        db =SessionLocal()
        try:
            manager =UserManager(db)
            try:
                user = manager.register(username, email, password)
            except ValueError as ve:
                return{"message":str(ve)},400
            return _serialize_user(user),201
        finally:
            db.close()

class LoginResource(Resource):
    def post(self):
        payload =request.get_json()
        username =payload.get("username")
        password =payload.get("password")
        if not username or not password:
            return{"message":"Missing required fields"},400
        db =SessionLocal()
        try:
            manager =UserManager(db)
            try:
                session = manager.login(username, password)
            except ValueError as ve:
                return{"message":str(ve)},400
            return{"token":session.token,"expires_at":session.expires_at.isoformat()},200
        finally:
            db.close()

class UsersResource(Resource):
    def get(self):
        db = SessionLocal()
        try:
            users = db.query(User).all()
            return jsonify([_serialize_user(user) for user in users])
        finally:
            db.close()