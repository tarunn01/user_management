from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from decorators.generate_token import token_required
from serializers.rule import RuleSchema
from services.rule_service import RuleService

rule_schema = RuleSchema()
rules_schema = RuleSchema(many=True)
rule_service = RuleService()

class RuleResource(Resource):
    # @token_required
    def get(self, current_user):
        user_rules =rule_service.get_rules_for_user(current_user.id)
        return rules_schema.dump(user_rules)

    def post(self,current_user):
        """create a rule for currently logged in user"""
        json_data =request.get_json()
        try:
            rule_data_object =rule_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        new_rule = rule_service.create_rule(rule_data_object,current_user.id)
        return{'message':'rule created','rule': rule_schema.dump(new_rule)}, 201