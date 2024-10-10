from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50))  # admin or client
    verified = db.Column(db.Boolean, default=False)  # Email verification status
    verification_token = db.Column(db.String(100), nullable=True)  # For email verification token

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    file = db.Column(db.String(200))  # Optional file attachment

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.String(500), nullable=False)
    file = db.Column(db.String(200))  # Optional file attachment
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#change