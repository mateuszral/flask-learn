from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from app.services.user_service import get_user_by_username, get_user_by_email, create_user, authenticate_user, get_user_by_username, get_user_by_email


auth = Blueprint('auth', __name__)

@auth.get('/login')
def login_form():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))
        
    return render_template('auth.html')

@auth.post('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')
    
    user = authenticate_user(email, password)
    
    if user: 
        login_user(user, remember=remember)

        if user.change_password:
            flash('Login successful! You have to change your password.', 'info')
            return redirect(url_for('profile.profile_security'))

        flash('Login successful!', 'success')
        return redirect(url_for('main.home'))
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@auth.get('/forgot-password')
@login_required
def forgot_password():
    return render_template('forgot_password.html')


@auth.post('/forgot-password')
@login_required
def forgot_password_form():
    email = request.form.get('email')
    
    if get_user_by_email(email):
        flash('Password reset link sent to your email (not really, this is a demo)', 'info')
        return render_template('auth.html')
    
    flash('Email not found', 'error')
    return render_template('auth.html')

@auth.get('/register')
def register_form():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))
        
    return render_template('auth.html')

@auth.post('/register')
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if get_user_by_email(email) or get_user_by_username(username):
        flash('User with username/email already exists', 'error')
        return render_template('auth.html')
        
    if password != confirm_password:
        flash('Passwords are not the same', 'error')
        return render_template('auth.html')
        
    user, message = create_user(username, email, password)
    
    if not user:
        flash(message, 'error')
    else:    
        flash('Account created successfully! You can now log in. Can change user info after login (first name, last name, age, bio)', 'success')
    return render_template('auth.html')

@auth.get('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))