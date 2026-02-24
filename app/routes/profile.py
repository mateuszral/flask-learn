import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from ..utils.utils import USERS, authenticate_user

profile = Blueprint('profile', __name__)

@profile.get('/profile')
def profile_view():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        return render_template('profile.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.post('/profile')
def profile_update():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        bio = request.form.get('bio')
        age = request.form.get('age')
        avatar = request.files.get('avatar')
        
        if user['username'] == username and user['email'] == email and user['user_info']['first_name'] == first_name and user['user_info']['last_name'] == last_name and user['user_info']['bio'] == bio and user['user_info']['age'] == age and not avatar:
            flash('No changes made to the account.', 'info')
            return redirect(url_for('profile.profile_view'))

        if any(u["username"] == username for u in USERS if u["id"] != session['user_id']):
            flash('Username already exists', 'error')
            return redirect(url_for('profile.profile_view'))

        if any(u["email"] == email for u in USERS if u["id"] != session['user_id']):
            flash('Email already exists', 'error')
            return redirect(url_for('profile.profile_view'))

        if first_name:
            user['user_info']['first_name'] = first_name
        if last_name:
            user['user_info']['last_name'] = last_name
        if bio:
            user['user_info']['bio'] = bio
            user['username'] = username
        if email:
            user['email'] = email
        if age:
            user['user_info']['age'] = age
            
        if avatar.filename != '':
            filename = secure_filename(avatar.filename)
            os.makedirs(os.path.join(f'app/{current_app.config["UPLOAD_FOLDER"]}'), exist_ok=True)
            upload_path = os.path.join(f'app/{current_app.config['UPLOAD_FOLDER']}', filename)
            avatar.save(upload_path)
            user['avatar'] = f'{current_app.config['UPLOAD_FOLDER']}/{filename}'
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile_view'))

    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.post('/delete-account')
def profile_delete():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        USERS.remove(user)
        session.clear()
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('main.home'))
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.get('/security')
def profile_security():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        return render_template('security.html', user=user)
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))

@profile.post('/change-password')
def profile_change_password():
    user = next((u for u in USERS if u['id'] == session['user_id']), None)
    if user:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not authenticate_user(user['email'], current_password, USERS):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('profile.profile_security'))
        
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('profile.profile_security'))
        
        if current_password == new_password:
            flash('New password cannot be the same as the current password', 'error')
            return redirect(url_for('profile.profile_security'))
        
        user['password'] = generate_password_hash(new_password)
        user['change_password'] = False
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile.profile_security'))
    
    flash('User not found', 'error')
    session.clear()
    return redirect(url_for('main.home'))