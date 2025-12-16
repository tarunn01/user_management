from init import ma
from models.user import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # load_instance = True # Removed this line
        # Exclude password_hash from the serialized output
        exclude = ("password_hash",)

    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    firstname = ma.auto_field(required=True)
    lastname = ma.auto_field(required=True)

    # This field is used only for loading/deserializing the password.
    # It will not be dumped/serialized.
    password = fields.Str(required=True, load_only=True)