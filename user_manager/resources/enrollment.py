from flask import request
from flask_restful import Resource
from decorators.generate_token import token_required
from services.enrollment_service import EnrollmentService

enrollment_service = EnrollmentService()

class EnrollmentResource(Resource):
    @token_required
    def post(self, current_user, action):
        """
        Handles POST requests for enrollment.
        URL: /api/enrollment/<action>
        Actions: 'start', 'verify'
        """
        if action == 'start':
            # Call service to generate code
            code = enrollment_service.start_enrollment(current_user.id)
            
            # In a real app, you would send this code via SMS/Email.
            # For testing, we return it in the response.
            return {'message': 'Enrollment started', 'code': code}, 200
        
        elif action == 'verify':
            data = request.get_json()
            code = data.get('code')
            device_id = data.get('device_id')
            
            if not code or not device_id:
                return {'message': 'Code and device_id are required'}, 400
                
            # Call service to verify
            success = enrollment_service.verify_enrollment(current_user.id, code, device_id)
            
            if success:
                return {'message': 'Enrollment verified successfully'}, 200
            else:
                return {'message': 'Invalid code or expired'}, 400
        
        return {'message': 'Invalid action'}, 404