# In extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_caching import Cache


# Initialize extensions without attaching them to an app yet
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
cache = Cache()