from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user
from werkzeug.security import check_password_hash

from app.services.user_service import get_user_by_email

def authenticate_user(email, password):
    user = get_user_by_email(email)

    if user and check_password_hash(user.password, password):
        return user

    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != "admin":
            abort(403)

        return f(*args, **kwargs)

    return decorated_function