# In serializers/user.py
from extensions import ma, db
from models.user import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # load_instance = True  <-- REMOVED THIS
        # We want a dictionary, not a User object, so we can handle password hashing easily
        sqla_session = db.session
        exclude = ("password_hash",)

    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    firstname = ma.auto_field(required=True)
    lastname = ma.auto_field(required=True)

    password = fields.Str(required=True, load_only=True)