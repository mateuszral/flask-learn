import uuid

from flask import flash, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


USERS = [
    {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@admin.com",
        "password": generate_password_hash("admin"),
        "role": "admin"
    },
    {
        "id": str(uuid.uuid4()),
        "username": "johndoe",
        "email": "john@example.com",
        "password": generate_password_hash("password123"),
        "role": "user"
    },
    {
        "id": str(uuid.uuid4()),
        "username": "janedoe",
        "email": "jane@example.com",
        "password": generate_password_hash("securepass"),
        "role": "user"
    }
]

def authenticate_user(email, password, users):
    user = next((u for u in users if u["email"] == email), None)

    if user and check_password_hash(user["password"], password):
        return user

    return None

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('login_form'))
        
        user = next((u for u in USERS if u['id'] == session['user_id']), None)
        if user and user['role'] == 'admin':
            return func(*args, **kwargs)
        
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))
    
    wrapper.__name__ = func.__name__
    return wrapper