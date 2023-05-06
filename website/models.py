from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedSerializer
from flask import current_app

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    rounds = db.relationship('Round')

    def generate_token(self):
        serial = TimedSerializer(current_app.config["SECRET_KEY"])
        return serial.dumps({"user_id":self.id})
    
    @staticmethod
    def verify_token(token):
        serial = TimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serial.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class Round(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(150))
    tees = db.Column(db.String(20))
    front_or_back = db.Column(db.String(10))
    slope = db.Column(db.Float)
    course_rating = db.Column(db.Float)
    date_played = db.Column(db.Date())
    score = db.Column(db.Integer)
    attestor = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

