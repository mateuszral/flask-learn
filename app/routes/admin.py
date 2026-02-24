import uuid

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from ..utils.utils import USERS, admin_required

admin = Blueprint('admin', __name__)

@admin.get('/user-management')
@admin_required
def user_management():
    return render_template('user_management.html', users=USERS)

@admin.get('/admin-panel')
@admin_required
def admin_panel():
    return render_template('admin_panel.html', users=USERS)

@admin.post('/admin/add-user')
@admin_required
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if any(u["email"] == email for u in USERS) or any(u["username"] == username for u in USERS):
        flash('User with username/email already exists', 'error')
        return redirect(url_for('admin.user_management'))

    new_user = {
        'id': str(uuid.uuid4()),
        'username': username,
        'email': email,
        'password': generate_password_hash(password),
        'role': role,
        'change_password': True,
        'featured': False,
        'user_info': {
            'first_name': '',
            'last_name': '',
            'age': 0,
            'bio': ''
        },
    }

    USERS.append(new_user)
    flash('User created successfully! Have to change password on first login', 'success')
    return redirect(url_for('admin.user_management'))

@admin.post('/edit-account/<user_id>')
@admin_required
def edit_account(user_id):
    if user_id == session['user_id']:
        flash('You cannot edit your own account from the admin panel. Use the edit profile option in your profile settings.', 'error')
        return redirect(url_for('admin.user_management'))
    
    user = next((u for u in USERS if u['id'] == user_id), None)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.user_management'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    bio = request.form.get('bio')
    age = request.form.get('age')
    featured = request.form.get('featured') == 'on'
    reset_password = request.form.get('resetPassword')
    reset_avatar = request.form.get('resetAvatar')
    
    if user['username'] == username and user['email'] == email and user['role'] == role and user['user_info']['first_name'] == first_name and user['user_info']['last_name'] == last_name and user['user_info']['bio'] == bio and user['user_info']['age'] == age and user['featured'] == featured and not reset_password and not reset_avatar:
        flash('No changes made to the account.', 'info')
        return redirect(url_for('admin.user_management'))

    if any(u["username"] == username for u in USERS if u["id"] != user_id):
        flash('Username already exists', 'error')
        return redirect(url_for('admin.user_management'))

    if any(u["email"] == email for u in USERS if u["id"] != user_id):
        flash('Email already exists', 'error')
        return redirect(url_for('admin.user_management'))

    if username:
        user['username'] = username
    if email:
        user['email'] = email    
    if role in ['user', 'admin']:
        user['role'] = role
    if first_name:
        user['user_info']['first_name'] = first_name
    if last_name:
        user['user_info']['last_name'] = last_name
    if bio:
        user['user_info']['bio'] = bio
    if age:
        user['user_info']['age'] = age
    if featured:
        user['featured'] = featured
    if reset_password:
        user['password'] = generate_password_hash('defaultpassword')
        user['change_password'] = True
    if reset_avatar:
        user['avatar'] = 'static/uploads/default.png'

    flash('Account updated successfully!', 'success')
    return redirect(url_for('admin.user_management'))

@admin.post('/delete-account/<user_id>')
def delete_account(user_id):
    if user_id == session['user_id']:
        flash('You cannot delete your own account from the admin panel. Use the delete account option in your profile settings.', 'error')
        return redirect(url_for('admin.user_management'))
        
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user:
        USERS.remove(user)
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found', 'error')
        
    return redirect(url_for('admin.user_management'))