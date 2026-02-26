from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.services.user_service import get_user_by_id, get_user_by_username, get_user_by_email, create_user, authenticate_user, get_user_by_username, get_user_by_email


auth = Blueprint('auth', __name__)

@auth.get('/login')
def login_form():
    if 'user_id' in session:
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
        session['user_id'] = user.id

        if remember:
            session.permanent = True
        else:
            session.permanent = False

        if user.change_password:
            flash('Login successful! You have to change your password.', 'info')
            return redirect(url_for('profile.profile_security'))

        flash('Login successful!', 'success')
        return redirect(url_for('main.home'))
    
    flash('Invalid credentials', 'error')
    return render_template('auth.html')

@auth.get('/forgot-password')
def forgot_password():
    if 'user_id' in session:
        return render_template('forgot_password.html')
    
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('auth.login_form'))


@auth.post('/forgot-password')
def forgot_password_form():
    email = request.form.get('email')
    
    if get_user_by_email(email):
        flash('Password reset link sent to your email (not really, this is a demo)', 'info')
        return render_template('auth.html')
    
    flash('Email not found', 'error')
    return render_template('auth.html')

@auth.get('/register')
def register_form():
    if 'user_id' in session:
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
        
    create_user(username, email, password)
    
    flash('Account created successfully! You can now log in. Can change user info after login (first name, last name, age, bio)', 'success')
    return render_template('auth.html')

@auth.get('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')