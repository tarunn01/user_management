import random
import string
from asyncio import timeout

from extensions import db,cache
from models.enrollment import UserEnrollment

class EnrollmentService:
    def start_enrollment(self,user_id):
        code = ''.join(random.choices(string.digits, k = 6))
        cache.set(f"enrollment:{user_id}", code, timeout =300)

        return code

    def verify_enrollment(self,user_id,code, device_id,):
        stored_code = cache.get(f"enrollment:{user_id}")
        if not stored_code or stored_code != code:
            return False
        #save to db
        enrollment = UserEnrollment(
            user_id = user_id,
            device_type = "mobile",
            device_id = device_id
        )
        db.session.add(enrollment)
        db.session.commit()
        cache.delete(f"enrollment: {user_id}") #cleanup
        return True