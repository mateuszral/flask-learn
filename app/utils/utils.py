from flask import flash, redirect, session, url_for
from werkzeug.security import check_password_hash

from app.services.user_service import get_user_by_email, get_user_by_id

def authenticate_user(email, password):
    user = get_user_by_email(email)

    if user and check_password_hash(user.password, password):
        return user

    return None

def admin_required(func):
    def wrapper(*args, **kwargs):
        user = get_user_by_id(session['user_id'])
        if not user:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('auth.login_form'))
        
        if user.role == 'admin':
            return func(*args, **kwargs)
        
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.home'))
    
    wrapper.__name__ = func.__name__
    return wrapper