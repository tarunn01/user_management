from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from resources.health import Health
from init import app, api
from resources.user import UserResource


api.add_resource(UserResource, '/users')
api.add_resource(Health, '/health')

if __name__ == '__main__':
    app.run(debug=True)
        