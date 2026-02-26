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
    if get_user_by_username(username) or get_user_by_email(email):
        return None, "User with username/email already exists"
    
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
    )
    
    db.session.add(user)
    db.session.commit()
    
    user_info = UserInfo(user_id=user.id)
    
    db.session.add(user_info)
    db.session.commit()
    
    return user, "User created successfully! Have to change password on first login"

def admin_create_user(username, email, password, role):
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.commit()
    
    user_info = UserInfo(user_id=user.id)
    db.session.add(user_info)
    db.session.commit()
    
    return user

def admin_edit_user(user_id, username, email, role, first_name, last_name, bio, age, featured, reset_password=False, reset_avatar=False):
    user = User.query.get(user_id)
    
    if not user:
        return None, "User not found"
    
    no_changes = (
        user.username == username and
        user.email == email and
        user.role == role and
        user.user_info.first_name == first_name and
        user.user_info.last_name == last_name and
        user.user_info.bio == bio and
        str(user.user_info.age) == str(age) and
        user.featured == featured and
        not reset_password and
        not reset_avatar
    )
    
    if no_changes:
        return user, "No changes made to the account."
    
    existing_username = User.query.filter(
        User.username == username,
        User.id != user_id
    ).first()

    if existing_username:
        return None, "Username already exists"

    existing_email = User.query.filter(
        User.email == email,
        User.id != user_id
    ).first()

    if existing_email:
        return None, "Email already exists"
    
    user.username = username
    user.email = email
    
    if role in ['user', 'admin']:
        user.role = role
    
    if reset_password:
        user.password = generate_password_hash('zaq1@WSX')
        user.change_password = True
    
    if reset_avatar:
        user.avatar = None
    
    user.user_info.first_name = first_name
    user.user_info.last_name = last_name
    user.user_info.bio = bio
    user.user_info.age = age
    user.featured = featured
    
    db.session.commit()
    
    return user, "Account updated successfully!"

def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None, "User not found"
    
    db.session.delete(user)
    db.session.commit()
    return user, "User deleted successfully!"