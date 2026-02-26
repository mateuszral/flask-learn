from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User, UserInfo


def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def authenticate_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user.password, password):
        return user
    
    return None

def create_user(username, email, password):
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
    )

    db.session.add(user)
    db.session.commit()
    
    return user

def delete_user(user_id):
    return User.query.filter_by(id=user_id).delete()