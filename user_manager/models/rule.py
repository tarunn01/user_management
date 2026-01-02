from extensions import db,ma,bcrypt
from models.user import User

class Rule(db.Model):
    __tablename__ = "Rule"
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(100),nullable = False)
    description = db.Column(db.String(255))

    user_id= db.Column(db.Integer,db.ForeignKey("users.id"),nullable= False)