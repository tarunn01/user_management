from init import ma
from models.rule import Rule

class RuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rule
        load_instance =True
        include_fk = True # including the user_id fk here