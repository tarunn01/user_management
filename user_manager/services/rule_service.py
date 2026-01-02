from init import db
from models.rule import Rule

class RuleService:
    def get_rules_for_user(self,user_id):
        return Rule.query.filter_by(user_id=user_id).all()

    def create_rule(self,rule_data,user_id):
        """create a new rule and associates with a user."""
        rule_data.user_id = user_id
        db.session.add(rule_data)
        db.session.commit()
        return rule_data