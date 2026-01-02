from extensions import db

class UserEnrollment(db.Model):
    __tablename__ = "user_enrollments"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
    device_type = db.Column(db.String(50), nullable = False)
    device_id = db.Column(db.String(100), unique = True,nullable = False)
    active = db.Column(db.Boolean, default = True)