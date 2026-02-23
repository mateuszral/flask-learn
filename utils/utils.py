from flask import flash, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


USERS = [
    {
        "id": "70676dfe-7b41-4972-8206-b470d365a82b",
        "username": "admin",
        "email": "admin@admin.com",
        "password": generate_password_hash("admin"),
        "role": "admin",
        "change_password": False
    },
    {
        "id": "fd14e866-209f-4422-ba1c-e499910e9d76",
        "username": "johndoe",
        "email": "john@example.com",
        "password": generate_password_hash("password123"),
        "role": "user",
        "change_password": False
    },
    {
        "id": "6c6590d6-a16f-444d-9e9b-b8de29e6174f",
        "username": "janedoe",
        "email": "jane@example.com",
        "password": generate_password_hash("securepass"),
        "role": "user",
        "change_password": False
    }
]

def authenticate_user(email, password, users):
    user = next((u for u in users if u["email"] == email), None)

    if user and check_password_hash(user["password"], password):
        return user

    return None

def admin_required(func):
    def wrapper(*args, **kwargs):
        user = next((u for u in USERS if u['id'] == session['user_id']), None)
        if not user:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('login_form'))
        
        if user['role'] == 'admin':
            return func(*args, **kwargs)
        
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))
    
    wrapper.__name__ = func.__name__
    return wrapper