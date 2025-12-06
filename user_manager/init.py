from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



    

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = '//postgres:Welcome%40123@localhost:5432/user_manager_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)