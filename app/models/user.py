import uuid

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    change_password = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(255), nullable=True)
    
    user_info = db.relationship('UserInfo', backref='user', uselist=False, cascade='all, delete-orphan')
    
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)