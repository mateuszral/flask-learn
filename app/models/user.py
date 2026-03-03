import uuid

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'app_user'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    change_password = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(255), nullable=True)
    joined_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    
    user_info = db.relationship('UserInfo', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('app_user.id', ondelete='CASCADE'), primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    user = db.relationship('User', back_populates='user_info')